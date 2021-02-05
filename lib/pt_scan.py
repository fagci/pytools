from typing import Callable, Iterator


def ips_with_port(ips: Iterator or list, port: int, workers: int = 16, timeout: float = 0.2, total=None):
    """Filter IPs by given port"""
    from lib.pt_network import portchecker
    check_port = portchecker(port, timeout)
    return filter_ips2(ips, check_port, workers, total)


def filter_ips2(ips: Iterator or list, filter_fn: Callable, workers: int = 16, total=None):
    """Filter IPs by callable, which must return falsy value"""
    from threading import Thread
    from queue import Queue, Empty
    from tqdm import tqdm
    from itertools import islice

    pb = tqdm(total=total, unit='ips')

    q_in = Queue()
    q_out = Queue()

    put = q_in.put_nowait
    get = q_out.get

    threads = []

    for ip in islice(ips, workers):
        put(ip)

    if isinstance(ips, list):
        del ips[:workers]

    args = (filter_fn, q_in, q_out, pb,)

    for _ in range(workers):
        thr = Thread(target=_process_q, daemon=True, args=args)
        threads.append(thr)

    for thr in threads:
        thr.start()

    for ip in ips:
        put(ip)

    while any(map(lambda t: t.is_alive(), threads)):
        try:
            yield get(timeout=7)
        except Empty:
            break

    while not q_out.empty():
        yield get()

    pb.close()


def _process_q(filter_fn, q_in, q_out, pb):
    get = q_in.get
    put = q_out.put_nowait
    done = q_in.task_done
    progress = pb.update

    while True:
        result = filter_fn(get())
        progress()

        if isinstance(result, tuple):
            if result[0]:
                put(result)
        elif result:
            put(result)

        done()
