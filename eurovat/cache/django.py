import eurovat
import datetime
import time
from typing import Dict

from django.core.cache import cache

class DjangoCache:
    cache_prefix: str
    mtime: float=0

    def __init__(self, cache_prefix: str):
        self.cache_prefix = cache_prefix

    @property
    def _cache_mtime_key(self):
        return f"{self.cache_prefix}_mtime"

    @property
    def _cache_data_key(self):
        return f"{self.cache_prefix}_data"

    def get_mtime(self) -> float:
        return cache.get(self._cache_mtime_key, 0)
    
    def load(self) -> Dict[str, object]:
        data = cache.get(self._cache_data_key)
        self.mtime = self.get_mtime()

        return data

    def save(self, data):
        cache.set(self._cache_data_key, data)
        cache.set(self._cache_mtime_key, time.time())
