from typing import Dict

class Cache:
    def get_mtime(self) -> float:
        raise NotImplementedError()

    def load(self) -> Dict[str, object]:
        raise NotImplementedError()

    def save(self, data: Dict[str, object]):
        raise NotImplementedError()
