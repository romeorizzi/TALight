import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("# Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def run_with_deadline(f,args,deadline):
    try:
        with time_limit(deadline):
            return (True, f(**args))
    except TimeoutException as e:
        print("Timed out!")
    return (False, None)


