import os
import fnmatch


class DirectoryTreeWalker:
    def __init__(self):
        self.file_count = 0
        self.dir_count = 0
        self.tree_output = ""
        self.file_contents = []

    def walk(self, directory, pattern=None, ignore_pattern=None, include_hidden=False):
        self._walk(directory, "", "", pattern, ignore_pattern, include_hidden)

    def _walk(self, full_path, relative_path, padding, pattern=None, ignore_pattern=None, include_hidden=False):
        if not os.path.isdir(full_path):
            return

        entries = sorted(os.listdir(full_path))
        total = len(entries)
        count = 0

        for entry in entries:
            if not include_hidden and entry.startswith('.'):
                continue
            
            entry_full_path = os.path.join(full_path, entry)
            entry_relative_path = os.path.join(relative_path, entry) if relative_path else entry
            
            count += 1
            if os.path.isdir(entry_full_path):
                if ignore_pattern and any(fnmatch.fnmatch(entry, p) for p in ignore_pattern):
                    continue
                self.output += f'{padding}{"└── " if count == total else "├── "}{entry}\n'
                self.dir_count += 1
                self._walk(entry_full_path, padding + ("    " if count == total else "│   "), pattern, ignore_pattern)
            elif os.path.isfile(entry_full_path):
                if (pattern and not any(fnmatch.fnmatch(entry, p) for p in pattern)) or \
                   (ignore_pattern and any(fnmatch.fnmatch(entry, p) for p in ignore_pattern)):
                    continue
                self.output += f'{padding}{"└── " if count == total else "├── "}{entry}\n'
                self.file_count += 1
                file_contents = self._read_file_contents(entry_full_path)
                self.file_contents.append(f'---\nFilePath: {entry_relative_path}\n---\n{file_contents}\n')
                
    def _read_file_contents(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f'Error reading file: {e}'


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
