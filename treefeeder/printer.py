from .tree import get_tree
from .contents import get_contents


def get_output(directory, pattern=None, ignore_pattern=None, include_hidden=False, separator=None):
    tree_output = get_tree(directory, pattern, ignore_pattern, include_hidden)
    contents_output = get_contents(directory, pattern, ignore_pattern, include_hidden)
    
    output = (separator + "\n").join([tree_output] + contents_output + [""])
    
    return output
