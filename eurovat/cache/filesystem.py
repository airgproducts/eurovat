import os
import json
from typing import Dict

from eurovat.cache.cache import Cache


class FilesystemCache(Cache):
    filename: str
    track_mtime: bool=True
    mtime: float=0

    def __init__(self, filename: str):
        self.filename = filename
    
    @property
    def has_changed(self):
        if not self.track_mtime:
            return False

        return self.get_mtime() > self.mtime

    def get_mtime(self) -> float:
        return os.path.getmtime(self.filename)
    
    def load(self) -> Dict[str, object]:
        with open(self.filename) as infile:
            data = json.load(infile)
        
        self.mtime = self.get_mtime()
        return data

    def save(self, data):
        with open(self.filename, "w") as outfile:
            json.dump(data, outfile, indent=2)
