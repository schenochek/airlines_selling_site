#fetch from cache внутри нее определен декоратор. возвращает имя декоратора
from functools import wraps
from cache.connection import RedisCache


def fetch_from_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis']) #connection to redis
    ttl = cache_config['ttl']

    def wrapper_func(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            cached_value = cache_conn.get_value(cache_name)#Извлекаем из кэша
            if cached_value:
                return cached_value
            response = f(*args, **kwargs)
            cache_conn.set_value(cache_name, response, ttl=ttl)
            return response
        return wrapper
    return wrapper_func
