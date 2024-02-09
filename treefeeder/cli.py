import argparse


def get_args():
    parser = argparse.ArgumentParser(description='List contents of directories in a tree-like format.')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to start listing')
    parser.add_argument('-P', '--pattern', action='append', help='List only those files that match the pattern')
    parser.add_argument('-I', '--ignore', action='append', help='Do not list files that match the given pattern')
    parser.add_argument('-S', '--separator', default='[SEP]', help='Separator to use between statements')
    return parser.parse_args()
