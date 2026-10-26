
from multiprocessing import Process
import time

def print_time(thread_name, delay, iterations):
    start = int(time.time())
    for i in range(iterations):
        time.sleep(delay)
        seconds_elapsed = str(int(time.time()) - start)
        print(thread_name if thread_name else seconds_elapsed)
