import os
from queue import Queue
import threading

def worker(q: Queue, n):
    while True:
        item = q.get(timeout=3)
        if item is None:
            break
        print(f'process data: {n}, {item}')


if __name__ == '__main__':
    q = Queue(5)
    os.wait()
    th1 = Thread(target=worker, args=(q, 1))
    th2 = Thread(target=worker, args=(q, 2))
    th1.start()
    th2.start()

    # for i in range(50):
    #     q.put(i)

    # q.put(None); q.put(None)
    th1.join(); th1.join()