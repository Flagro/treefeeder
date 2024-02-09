import os
import fnmatch


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
        self._walk(directory, "", "")

    def _walk(self, full_path, relative_path, padding):
        if not os.path.isdir(full_path):
            return

        entries = sorted(os.listdir(full_path))
        total = len(entries)
        count = 0

        for entry in entries:
            if not self.include_hidden and entry.startswith('.'):
                continue
            
            entry_full_path = os.path.join(full_path, entry)
            entry_relative_path = os.path.join(relative_path, entry) if relative_path else entry
            
            count += 1
            if os.path.isdir(entry_full_path):
                if self.ignore_pattern and any(fnmatch.fnmatch(entry, p) for p in self.ignore_pattern):
                    continue
                self.output += f'{padding}{"└── " if count == total else "├── "}{entry}\n'
                self.dir_count += 1
                self._walk(entry_full_path, padding + ("    " if count == total else "│   "), self.pattern, self.ignore_pattern)
            elif os.path.isfile(entry_full_path):
                if (self.pattern and not any(fnmatch.fnmatch(entry, p) for p in self.pattern)) or \
                   (self.ignore_pattern and any(fnmatch.fnmatch(entry, p) for p in self.ignore_pattern)):
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
            return 'Error reading file: {}'.format(str(e))


def get_output(directory, pattern=None, ignore_pattern=None, include_hidden=False, separator=None):
    walker = DirectoryTreeWalker(pattern, ignore_pattern, include_hidden)
    walker.walk(directory)
    tree_output = f"{walker.output}\n\n{walker.dir_count} directories, {walker.file_count} files\n"
    contents_output = walker.file_contents
    
    output = (separator + "\n").join([tree_output] + contents_output + [""])
    
    return output
