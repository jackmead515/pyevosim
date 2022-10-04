from symbol import decorator
import time


_profile_map = {}


def profile(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            
            if name not in _profile_map:
                _profile_map[name] = { 'count': 0, 'time': elapsed }
            
            _profile_map[name]['count'] += 1
            _profile_map[name]['time'] = elapsed

            print(f"{name}: {elapsed*1000:.2f}ms")

            return result
        return wrapper
    return decorator


def print_profiles():
    for name, data in _profile_map.items():
        print(f"{name}: {data['time']*1000:.2f}ms ({data['count']})")