from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable

from tqdm import tqdm

from lib.pt_network import portchecker


def ips_with_port(ips: Iterable, port: int, workers: int = None, timeout: float = 0.2, total=None):
    """Filter IPs by given port"""
    check_port = portchecker(port, timeout)
    return filter_ips2(ips, check_port, workers, total)


def filter_ips(ips: Iterable, filter_fn: Callable, workers: int = None, total=None):
    """Filter IPs by callable, which must return falsy value"""
    with ThreadPoolExecutor(workers) as executor:
        for result in tqdm(executor.map(filter_fn, ips), total=total, unit='ips'):
            if isinstance(result, tuple):
                if result[0]:
                    yield result
            elif result:
                yield result


def filter_ips2(ips: Iterable, filter_fn: Callable, workers: int = None, total=None):
    """Filter IPs by callable, which must return falsy value"""
    from threading import Thread, Lock
    from queue import Queue, Empty
    lock = Lock()
    qin = Queue()
    qout = Queue()
    pb = tqdm(total=total, unit='ips')

    def proc():
        while True:
            ip = qin.get()
            if ip is None:
                qout.put(None)
                qin.task_done()
                pb.close()
                break
            with lock:
                pb.update(1)

            result = filter_fn(ip)
            if isinstance(result, tuple):
                if result[0]:
                    qout.put(result)
            elif result:
                qout.put(result)

            qin.task_done()

    for ip in ips:
        qin.put(ip)

    qin.put(None)

    for _ in range(workers or 16):
        thr = Thread(target=proc)
        thr.daemon = True
        thr.start()

    while True:
        try:
            res = qout.get()
            if res is None:
                break
            yield res
        except Empty:
            break
