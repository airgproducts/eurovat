from typing import Dict

class Cache:
    def get_mtime(self) -> float:
        return cache.get(self._cache_mtime_key)

    def load(self) -> Dict[str, object]:
        raise NotImplementedError()

    def save(self, data: Dict[str, object]):
        raise NotImplementedError()
