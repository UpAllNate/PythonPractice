from threading import Thread
from time import perf_counter, sleep
import sys
from random import random
from enum import Enum, auto as enum_auto

TIME_MIN = 0.5
TIME_MAX = 2.5
WAIT_THREAD_COUNT = 3

class Thread_Kill_Index:
    waiter = [i+1 for i in range(WAIT_THREAD_COUNT)]

wait_kill_code = [False for _ in range(WAIT_THREAD_COUNT + 1)] # + 1 because enum_auto() starts with 1
threads = [Thread() for _ in range(WAIT_THREAD_COUNT + 1)] 

def wait_for_time(duration, kill_index):
    global wait_kill_code
    print(f"running wait thread index {kill_index}")
    start = perf_counter()
    sleep(duration)
    end = perf_counter()
    print(f"completed wait {duration}, actual duration: {end - start}")
    if wait_kill_code[kill_index]:
        print("woops! Ok, ok, sorry.")
        sys.exit()

def wait_controller():
    global threads, wait_kill_code

    print("top of wait_controller")
    
    for i in range(WAIT_THREAD_COUNT):
        thread_index = i + 1
        if not threads[thread_index].is_alive():
            wait_duration = TIME_MIN + (TIME_MAX - TIME_MIN) * random()
            print(f"running wait for time: {wait_duration}")
            threads[thread_index] = Thread(target=wait_for_time, args=(wait_duration, Thread_Kill_Index.waiter[i]))
            threads[thread_index].start()
    sleep(0.1)

if __name__ == "__main__":

    while True:
        try:
            wait_controller()

        # Shut down all threads when it's time to close the program
        except KeyboardInterrupt as e:
            print(f"Keyboard Interrupt: {e}")
            wait_kill_code = [True for _ in range(WAIT_THREAD_COUNT + 1)]
            for t in threads:
                if t.is_alive():
                    t.join()
            raise KeyboardInterrupt

