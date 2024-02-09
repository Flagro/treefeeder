import os
import fnmatch


class DirectoryTreeWalker:
    def __init__(self):
        self.file_count = 0
        self.dir_count = 0
        self.output = ""

    def walk(self, directory, pattern=None, ignore_pattern=None):
        self._walk(directory, "", pattern, ignore_pattern)

    def _walk(self, directory, padding, pattern=None, ignore_pattern=None, print_files=True):
        if not os.path.isdir(directory):
            return

        files = []
        if print_files:
            files = [f for f in sorted(os.listdir(directory)) if os.path.isfile(os.path.join(directory, f))]
        dirs = [d for d in sorted(os.listdir(directory)) if os.path.isdir(os.path.join(directory, d))]

        count = 0
        total = len(dirs) + (len(files) if print_files else 0)
        for d in dirs:
            count += 1
            path = os.path.join(directory, d)
            if ignore_pattern and any(fnmatch.fnmatch(d, p) for p in ignore_pattern):
                continue
            self.output += f'{padding}{"└── " if count == total else "├── "}{d}\n'
            self.dir_count += 1
            self._walk(path, padding + ("    " if count == total else "│   "), pattern, ignore_pattern)

        if print_files:
            for f in files:
                count += 1
                if pattern and not any(fnmatch.fnmatch(f, p) for p in pattern):
                    continue
                if ignore_pattern and any(fnmatch.fnmatch(f, p) for p in ignore_pattern):
                    continue
                self.output += f'{padding}{"└── " if count == total else "├── "}{f}\n'
                self.file_count += 1


def get_tree(directory, pattern=None, ignore_pattern=None):
    """
    Get the tree representation of the directory.

    :param directory: The directory to list
    :param prefix: The prefix to use for the tree
    :param pattern: List only those files that match the pattern
    :param ignore_pattern: Do not list files that match the given pattern
    :return: The tree representation of the directory
    """
    walker = DirectoryTreeWalker(directory, pattern, ignore_pattern)
    walker.walk()
    output = f"{walker.output}\n\n{walker.dir_count} directories, {walker.file_count} files\n"
    return output
