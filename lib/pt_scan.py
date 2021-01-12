from typing import Callable, Iterable


def ips_with_port(ips: Iterable, port: int, workers: int = None, timeout: float = 0.2, total=None):
    """Filter IPs by given port"""
    from lib.pt_network import portchecker
    check_port = portchecker(port, timeout)
    return filter_ips2(ips, check_port, workers, total)


def filter_ips2(ips: Iterable, filter_fn: Callable, workers: int = None, total=None):
    """Filter IPs by callable, which must return falsy value"""
    from threading import Thread
    from queue import Queue, Empty
    from tqdm import tqdm

    pb = tqdm(total=total, unit='ips')

    q_in = Queue()
    q_out = Queue()

    threads = []

    args = (filter_fn, q_in, q_out, pb,)

    for _ in range(workers or 16):
        thr = Thread(target=_process_q, daemon=True, args=args)
        threads.append(thr)

    for thr in threads:
        thr.start()

    for ip in ips:
        q_in.put(ip)

    while any(map(lambda t: t.is_alive(), threads)):
        try:
            yield q_out.get(timeout=5)
        except Empty:
            break

    while not q_out.empty():
        yield q_out.get()

    pb.close()


def _process_q(filter_fn, q_in, q_out, pb):
    while True:
        result = filter_fn(q_in.get())
        pb.update()

        if isinstance(result, tuple):
            if result[0]:
                q_out.put(result)
        elif result:
            q_out.put(result)

        q_in.task_done()
