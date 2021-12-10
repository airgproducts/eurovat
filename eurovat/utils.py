import os

package_dir = os.path.dirname(os.path.abspath(__file__))

def package_filename(filename: str) -> str:
    return os.path.join(package_dir, filename)


