# treefeeder

![treefeeder logo](https://github.com/Flagro/treefeeder/blob/main/logo.png?raw=true)

## About
`treefeeder` is a command-line interface (CLI) tool designed to transform a folder of files, such as code files, into a structured string. This string includes both the folder structure (in a Unix tree structure format) and the contents of the files. It's an ideal tool for feeding data into ChatGPT or other large language model (LLM) AI assistants for fine-tuning or query answering.

## Installation
To install `treefeeder`, simply run:
```bash
pip install treefeeder
```

## Usage

### CLI
You can use treefeeder from the command line by passing the directory path along with optional arguments for customization:

```bash
treefeeder <directory_path> [-I ignore_patterns] [-P match_patterns] [-S separator_token]
```
- <directory_path>: The path to the directory you want to process.
- -I ignore_patterns: Patterns to ignore files or directories.
- -P match_patterns: Patterns to match specific files.
- -S separator_token: The separator token used in output (default is [SEP]).

### Python API
treefeeder can also be used within Python. To get a string output of your folder structure and file contents, use:

```python
from treefeeder import get_output

output = get_output(directory_path, ignore_patterns=None, match_patterns=None, separator_token='[SEP]')
```

### Example

```bash
treefeeder /path/to/my_project -I *.log -P *.py -S "[SEP]"
```

This command will process the 'my_project' directory, ignore .log files, match .py files, and use [SEP] as the separator token.

## Contributing

Contributions are welcome! Please feel free to submit pull requests, suggest features, or report bugs.

## License

treefeeder is open-source and available under MIT License.
