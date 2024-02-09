import os
import fnmatch
from typing import List


class DirectoryContentsWalker:
    def __init__(self):
        self.output = []

    def walk(self, directory, pattern=None, ignore_pattern=None, include_hidden=False):
        self._walk(directory, '', pattern, ignore_pattern, include_hidden)

    def _walk(self, full_path, relative_path, pattern=None, ignore_pattern=None, include_hidden=False):
        if not os.path.isdir(full_path):
            return

        entries = sorted(os.listdir(full_path))

        for entry in entries:
            if not self.include_hidden and entry.startswith('.'):
                continue
            entry_full_path = os.path.join(full_path, entry)
            entry_relative_path = os.path.join(relative_path, entry) if relative_path else entry

            if os.path.isdir(entry_full_path):
                if ignore_pattern and any(fnmatch.fnmatch(entry, p) for p in ignore_pattern):
                    continue
                self._walk(entry_full_path, entry_relative_path, pattern, ignore_pattern)
            elif os.path.isfile(entry_full_path):
                if (pattern and not any(fnmatch.fnmatch(entry, p) for p in pattern)) or \
                   (ignore_pattern and any(fnmatch.fnmatch(entry, p) for p in ignore_pattern)):
                    continue
                file_contents = self._read_file_contents(entry_full_path)
                self.output.append(f'---\nFilePath: {entry_relative_path}\n---\n{file_contents}\n')
    
    def _read_file_contents(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f'Error reading file: {e}'


def get_contents(directory, pattern=None, ignore_pattern=None, include_hidden=False) -> List[str]:
    """
    Get file contents of a directory as a list.

    :param directory: The directory to list
    :param pattern: List only those files that match the pattern
    :param ignore_pattern: Do not list files that match the given pattern
    :return: The contents of the directory as a list
    """
    walker = DirectoryContentsWalker()
    walker.walk(directory, pattern, ignore_pattern, include_hidden)
    return walker.output
