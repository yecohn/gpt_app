import time

def timeit(fun): 
    def wrapper(*args, **kwargs): 
        start = time.time()
        fun(*args, **kwargs)
        end = time.time()
        print(f"compute time: {end - start}")
    return wrapper


        