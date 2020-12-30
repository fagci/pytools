from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def thread_exec(fn, iterable, unit='it', threads='4'):
    with ThreadPoolExecutor(threads) as execuutor:
        return tqdm(execuutor.map(fn, iterable), total=len(iterable), unit=unit)

