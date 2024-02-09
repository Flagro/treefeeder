import fnmatch
from pathlib import Path

class DirectoryTreeWalker:
    def __init__(self, pattern=None, ignore_pattern=None, include_hidden=False):
        self.file_count = 0
        self.dir_count = 0
        self.tree_output = ""
        self.file_contents = []
        
        self.pattern = pattern
        self.ignore_pattern = ignore_pattern
        self.include_hidden = include_hidden

    def walk(self, directory):
        self._walk(Path(directory), "")

    def _walk(self, path, padding):
        if not path.is_dir():
            return

        entries = sorted(path.iterdir(), key=lambda x: x.name)
        total = len(entries)

        for count, entry in enumerate(entries, start=1):
            if not self.include_hidden and entry.name.startswith('.'):
                continue
            
            if self.ignore_pattern and any(fnmatch.fnmatch(entry.name, p) for p in self.ignore_pattern):
                continue
            
            if entry.is_file() and self.pattern and not any(fnmatch.fnmatch(entry.name, p) for p in self.pattern):
                continue

            connector = "└── " if count == total else "├── "
            self.tree_output += f'{padding}{connector}{entry.name}\n'

            if entry.is_dir():
                self.dir_count += 1
                self._walk(entry, padding + ("    " if count == total else "│   "))
            elif entry.is_file():
                self.file_count += 1
                file_contents = self._read_file_contents(entry)
                self.file_contents.append(f'---\nFilePath: {entry.relative_to(path.parent)}\n---\n{file_contents}\n')
                
    def _read_file_contents(self, file_path):
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            return 'Error reading file: {}'.format(str(e))


def get_output(directory, pattern=None, ignore_pattern=None, include_hidden=False, separator=None):
    walker = DirectoryTreeWalker(pattern, ignore_pattern, include_hidden)
    walker.walk(directory)
    tree_output = f"{walker.output}\n\n{walker.dir_count} directories, {walker.file_count} files\n"
    contents_output = walker.file_contents
    
    output = (separator + "\n").join([tree_output] + contents_output + [""])
    
    return output
