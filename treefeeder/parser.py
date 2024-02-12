"""
Parser module to walk through the directory tree and list the contents in a tree-like format.
"""

import fnmatch
from pathlib import Path
from typing import List, Optional


class DirectoryTreeWalker:
    """
    Walk through the directory tree and list the contents in a tree-like format.
    """

    def __init__(
        self,
        pattern: Optional[List[str]] = None,
        ignore_pattern: Optional[List[str]] = None,
        include_hidden: bool = False,
    ):
        """
        Initialize the DirectoryTreeWalker object.

        Args:
            pattern (Optional[List[str]]): List of file patterns to include.
            ignore_pattern (Optional[List[str]]): List of file patterns to ignore.
            include_hidden (bool): Flag to include hidden files/directories.

        Attributes:
            file_count (int): Number of files encountered during the walk.
            dir_count (int): Number of directories encountered during the walk.
            tree_output (str): Output string representing the directory tree.
            file_contents (List[str]): List of file contents encountered during the walk.
        """
        self.file_count = 0
        self.dir_count = 0
        self.tree_output = ""
        self.file_contents = []

        self.pattern = pattern
        self.ignore_pattern = ignore_pattern
        self.include_hidden = include_hidden

    def walk(self, path: Path, padding: str):
        """
        Recursively walk through the directory tree.

        Args:
            path (Path): The current path being traversed.
            padding (str): Padding string for formatting the tree output.
        """
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
                self.walk(entry, new_padding)
            elif entry.is_file():
                self.file_count += 1
                self._process_file(entry, path)

    def _filter_entries(self, entries: List[Path]) -> List[Path]:
        """
        Filter the entries based on the include and ignore patterns.

        Args:
            entries (List[Path]): List of entries to filter.

        Returns:
            List[Path]: Filtered list of entries.
        """
        return [entry for entry in entries if self._should_include(entry)]

    def _should_include(self, entry: Path) -> bool:
        """
        Check if the entry should be included based on the include and ignore patterns.

        Args:
            entry (Path): The entry to check.

        Returns:
            bool: True if the entry should be included, False otherwise.
        """
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
        """
        Process a file entry.

        Args:
            entry (Path): The file entry to process.
            parent_path (Path): The parent path of the file entry.
        """
        file_contents = self._read_file_contents(entry)
        file_relative_path = entry.relative_to(parent_path.parent)
        self.file_contents.append((file_relative_path, file_contents))

    def _read_file_contents(self, file_path: Path) -> str:
        """
        Read the contents of a file.

        Args:
            file_path (Path): The path of the file to read.

        Returns:
            str: The contents of the file.
        """
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
    """
    Get the output of the directory tree walk.

    Args:
        directory (str): The root directory to start the walk from.
        pattern (Optional[List[str]]): List of file patterns to include.
        ignore_pattern (Optional[List[str]]): List of file patterns to ignore.
        include_hidden (bool): Flag to include hidden files/directories.
        separator (Optional[str]): Separator string to join the output sections.

    Returns:
        str: The output of the directory tree walk.
    """
    walker = DirectoryTreeWalker(pattern, ignore_pattern, include_hidden)
    walker.walk(directory, "")
    tree_output = (
        f"{walker.tree_output}\n"
        + f"{walker.dir_count} directories, {walker.file_count} files\n"
    )
    contents_output = "".join(
        f"---\nFilePath: {file_content[0]}\n---\n{file_content[1]}\n"
        for file_content in walker.file_contents
    )
    separator = separator if separator else ""
    separator += "\n"
    output = separator.join([tree_output] + contents_output + [""])
    return output
