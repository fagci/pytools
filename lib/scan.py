from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable

from lib.network import portchecker


def ips_with_port(ips: Iterable, port: int, workers: int = None, timeout: float = 0.2, result_fn: Callable = lambda r: r):
    """Filter IPs by given port"""
    check_port = portchecker(port, timeout)
    return filter_ips(ips, check_port, workers, result_fn)


def filter_ips(ips: Iterable, filter_fn: Callable, workers: int = None, result_fn: Callable = lambda r: r):
    """Filter IPs by callable, which must return falsy value"""
    with ThreadPoolExecutor(workers) as executor:
        ips = [ip for ip in result_fn(executor.map(filter_fn, ips)) if ip]
        return ips
