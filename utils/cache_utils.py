from functools import lru_cache
from flask import request
import time


def cached(timeout, maxsize=128):
    """Декоратор для добавления кэширования к функции с учетом времени жизни кэша."""
    cache = {}

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Получаем endpoint для текущего запроса
            endpoint = request.endpoint  # Имя эндпоинта (route name)

            key = (endpoint, args, tuple(kwargs.items()))  # Ключ теперь включает endpoint

            if key in cache and time.time() - cache[key]['timestamp'] < timeout:
                return cache[key]['value']  # Возвращаем кэшированное значение

            value = func(*args, **kwargs)  # Вызываем функцию, если нет в кэше или устарел
            cache[key] = {'value': value, 'timestamp': time.time()}  # Кэшируем результат
            return value

        return wrapper
    return decorator