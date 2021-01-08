from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable

from tqdm import tqdm

from lib.pt_network import portchecker


def ips_with_port(ips: Iterable, port: int, workers: int = None, timeout: float = 0.2, total=None):
    """Filter IPs by given port"""
    check_port = portchecker(port, timeout)
    return filter_ips(ips, check_port, workers, total)


def filter_ips(ips: Iterable, filter_fn: Callable, workers: int = None, total=None):
    """Filter IPs by callable, which must return falsy value"""
    with ThreadPoolExecutor(workers) as executor:
        for result in tqdm(executor.map(filter_fn, ips), total=total, unit='ips'):
            if isinstance(result, tuple):
                if result[0]:
                    yield result
            elif result:
                yield result
