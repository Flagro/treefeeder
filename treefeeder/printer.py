from .tree import get_tree
from .contents import get_contents


def get_output(directory, pattern=None, ignore_pattern=None, separator=None):
    tree_output = get_tree(directory, pattern, ignore_pattern)
    contents_output = get_contents(directory, pattern, ignore_pattern)
    
    output = (separator + "\n").join([tree_output] + contents_output + ["User's query:"])
    
    return output
