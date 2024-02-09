import os
import fnmatch


class DirectoryTreeWalker:
    def __init__(self):
        self.file_count = 0
        self.dir_count = 0
        self.output = ""

    def walk(self, directory, pattern=None, ignore_pattern=None, include_hidden=False):
        self._walk(directory, "", pattern, ignore_pattern, include_hidden)

    def _walk(self, directory, padding, pattern=None, ignore_pattern=None, include_hidden=False):
        if not os.path.isdir(directory):
            return

        entries = sorted(os.listdir(directory))
        total = len(entries)
        count = 0

        for entry in entries:
            if not include_hidden and entry.startswith('.'):
                continue
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


def get_tree(directory, pattern=None, ignore_pattern=None, include_hidden=False) -> str:
    """
    Get the tree representation of the directory.

    :param directory: The directory to list
    :param pattern: List only those files that match the pattern
    :param ignore_pattern: Do not list files that match the given pattern
    :return: The tree representation of the directory
    """
    walker = DirectoryTreeWalker()
    walker.walk(directory, pattern, ignore_pattern, include_hidden)
    output = f"{walker.output}\n\n{walker.dir_count} directories, {walker.file_count} files\n"
    return output
