import fnmatch
from pathlib import Path
from typing import List, Optional


class DirectoryTreeWalker:
    def __init__(
        self,
        pattern: Optional[List[str]] = None,
        ignore_pattern: Optional[List[str]] = None,
        include_hidden: bool = False,
    ):
        self.file_count = 0
        self.dir_count = 0
        self.tree_output = ""
        self.file_contents = []

        self.pattern = pattern
        self.ignore_pattern = ignore_pattern
        self.include_hidden = include_hidden

    def walk(self, directory: str):
        self._walk(Path(directory), "")

    def _walk(self, path: Path, padding: str):
        if not path.is_dir():
            return

        entries = sorted(path.iterdir(), key=lambda x: x.name)
        filtered_entries = self._filter_entries(entries)
        total = len(filtered_entries)

        for count, entry in enumerate(filtered_entries, start=1):
            connector = "└── " if count == total else "├── "
            self.tree_output += f"{padding}{connector}{entry.name}\n"

            if entry.is_dir():
                self.dir_count += 1
                new_padding = padding + ("    " if count == total else "│   ")
                self._walk(entry, new_padding)
            elif entry.is_file():
                self.file_count += 1
                self._process_file(entry, path)

    def _filter_entries(self, entries: List[Path]) -> List[Path]:
        return [entry for entry in entries if self._should_include(entry)]

    def _should_include(self, entry: Path) -> bool:
        if not self.include_hidden and entry.name.startswith("."):
            return False
        if self.ignore_pattern and any(
            fnmatch.fnmatch(entry.name, p) for p in self.ignore_pattern
        ):
            return False
        if (
            entry.is_file()
            and self.pattern
            and not any(fnmatch.fnmatch(entry.name, p) for p in self.pattern)
        ):
            return False
        return True

    def _process_file(self, entry: Path, parent_path: Path):
        file_contents = self._read_file_contents(entry)
        self.file_contents.append(
            f"---\nFilePath: {entry.relative_to(parent_path.parent)}\n---\n{file_contents}\n"
        )

    def _read_file_contents(self, file_path: Path) -> str:
        try:
            return file_path.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file: {e}"


def get_output(
    directory: str,
    pattern: Optional[List[str]] = None,
    ignore_pattern: Optional[List[str]] = None,
    include_hidden: bool = False,
    separator: Optional[str] = None,
) -> str:
    walker = DirectoryTreeWalker(pattern, ignore_pattern, include_hidden)
    walker.walk(directory)
    tree_output = f"{walker.tree_output}\n\n{walker.dir_count} directories, {walker.file_count} files\n"
    contents_output = walker.file_contents
    separator = separator if separator else ""
    output = separator.join([tree_output] + contents_output + [""])
    return output
