from time import time, sleep
from functools import wraps

def _log(message):
    print('[timer] {function_name} {total_time:.3f}s'.format(**message))


def simple_time_tracker(log_fun=_log):
    def _simple_time_tracker(fn):
        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            start_time = time()

            try:
                result = fn(*args, **kwargs)
            finally:
                elapsed_time = time() - start_time

                # log the result
                log_fun({
                    'function_name': fn.__name__,
                    'total_time': elapsed_time,
                })
                
            return result

        return wrapped_fn
    return _simple_time_tracker

@simple_time_tracker()
def test_function():
    sleep(1)


if __name__ == "__main__":
    test_function()