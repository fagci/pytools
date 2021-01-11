from concurrent import futures
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
    ips_i = iter(ips)

    def proc():
        while True:
            ip = qin.get()
            with lock:
                pb.update(1)
            result = filter_fn(ip)

            if isinstance(result, tuple):
                if result[0]:
                    qout.put(result)
            elif result:
                qout.put(result)

            qin.task_done()

    def putter():
        while True:
            try:
                ip = next(ips_i)
                qin.put(ip)
            except StopIteration:
                break
    p = Thread(target=putter, daemon=True)
    p.start()

    threads = [Thread(target=proc) for _ in range(workers or 16)]

    for thr in threads:
        thr.daemon = True
        thr.start()

    while any(map(lambda t: t.is_alive(), threads)):
        try:
            res = qout.get(timeout=5)
            qout.task_done()
            yield res
        except Empty:
            break
    pb.close()
