from functools import update_wrapper
import time


def profiler(func):  # type: ignore
    """
    Returns profiling decorator, which counts calls of function
    and measure last function execution time.
    Results are stored as function attributes: `calls`, `last_time_taken`
    :param func: function to decorate
    :return: decorator, which wraps any function passed
    """
    profiler.counter = 0
    profiler.last_time_taken = 0

    def new(*args):
        new.last_time_taken = 0
        if profiler.counter == 0:
            new.calls = 0
            profiler.last_time_taken = time.time()
        new.calls += 1
        profiler.counter += 1
        a = func(*args)
        profiler.counter -= 1
        if profiler.counter == 0:
            new.last_time_taken = (time.time() - profiler.last_time_taken)
        return a

    new.calls = 0
    update_wrapper(new, func)
    return new
