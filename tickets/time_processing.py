import time
from functools import wraps

from tickets.serializers import RequestTimeSerializer


def measure_time(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        round_elapsed = elapsed.__round__(2)
        obj = {
            'processing_time': round_elapsed
        }
        serializer = RequestTimeSerializer(data=obj)
        if serializer.is_valid():
            serializer.save()
            print(f'Executed {func} in {elapsed:0.2f} seconds')
        return result

    return wrap
