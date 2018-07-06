import time

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        end = time.time()
        print(str(func) + " took " + str(end - start) + "s to run.")
        return rv
    return wrapper