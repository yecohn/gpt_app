import time

def timeit(fun):
    def wrapper(*args, **kwargs):
        start = time.time()
        output = fun(*args, **kwargs)
        end = time.time()
        print(f"compute time: {end - start}")
        return output
    return wrapper
