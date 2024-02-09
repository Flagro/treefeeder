from .tree import get_tree
from .contents import get_contents


def get_output(directory, prefix, pattern=None, ignore_pattern=None):
    tree_output = get_tree(directory, prefix, pattern, ignore_pattern)
    contents_output = get_contents(directory, pattern, ignore_pattern)
    return tree_output + contents_output
