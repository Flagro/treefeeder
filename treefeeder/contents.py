import os
import fnmatch
from typing import List


class DirectoryContentsWalker:
    def __init__(self):
        self.output = []

    def walk(self, directory, pattern=None, ignore_pattern=None):
        self._walk(directory, pattern, ignore_pattern)

    def _walk(self, directory, pattern=None, ignore_pattern=None):
        if not os.path.isdir(directory):
            return

        entries = sorted(os.listdir(directory))
        total = len(entries)
        count = 0

        for entry in entries:
            count += 1
            path = os.path.join(directory, entry)
            if os.path.isdir(path):
                if ignore_pattern and any(fnmatch.fnmatch(entry, p) for p in ignore_pattern):
                    continue
                self.output += f'{padding}{"└── " if count == total else "├── "}{entry}\n'
                self.dir_count += 1
                self._walk(path, padding + ("    " if count == total else "│   "), pattern, ignore_pattern)
            elif os.path.isfile(path):
                if (pattern and not any(fnmatch.fnmatch(entry, p) for p in pattern)) or \
                   (ignore_pattern and any(fnmatch.fnmatch(entry, p) for p in ignore_pattern)):
                    continue
                self.output += f'{padding}{"└── " if count == total else "├── "}{entry}\n'
                self.file_count += 1


def get_contents(directory, pattern=None, ignore_pattern=None) -> List[str]:
    """
    Get file contents of a directory as a list.

    :param directory: The directory to list
    :param pattern: List only those files that match the pattern
    :param ignore_pattern: Do not list files that match the given pattern
    :return: The contents of the directory as a list
    """
    walker = DirectoryContentsWalker(directory, pattern, ignore_pattern)
    walker.walk()
    return walker.output
