import time
from datetime import datetime

def track_time(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
            finally:
                end_time = time.time()
                elapsed_time = end_time - start_time
                try:
                    with open(filename, 'w') as file:
                        file.write(f"{elapsed_time:.4f}")
                except IOError as e:
                    print(f"Error writing to log file {filename}: {e}")
            return result
        return wrapper
    return decorator

def read_execution_times(file_name):
    # with open('execution_times.txt', 'r') as file:
    with open(file_name, 'r') as file:
        contents = file.readlines()
    return contents