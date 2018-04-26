"""TreeParser class"""
from pathlib import Path
import re


class TreeParser:
    """Reads a given tree structure and returns a dataframe"""
    def __init__(self, directory_format=None, file_regex=None):
        """Defines the directory and file format of the parser

        Parameters
        ----------
        directory_format : string
            The format is a regular expression. The names of the fields are
            given by named groups: `(?P<name>...)` other groups are discarded.
        file_regex : Dict[regex,column_name]
            regex is searched for in each file, and the result of the match is
            placed in the column
        """
        self.dir_format = []
        for i, dirname in enumerate(directory_format.split('/')):
            self.dir_format[i] = dirname
        self.file_regex = {re.compile(p): col for p, col in file_regex.items()}

    def parse(self, root_dir):
        """Parses the given root dir, returns the csv"""
        current_dir = Path(root_dir).expanduser()
        partial_results = {}
        partial_results[current_dir] = {}
        for cur_format in self.dir_format:
            partial_results = self._parse_dir(
                cur_format, partial_results)
        self._parse_files(partial_results)

    def _parse_dir(self, dir_format, partial_results):
        next_results = {}
        for current_dir, old_result in partial_results.items():
            for file_or_dir in current_dir.iterdir():
                res = re.match(dir_format, file_or_dir)
                if res:
                    self.next_results[file_or_dir] = {
                        **old_result, **res.groupdict()}
        return next_results

    def _parse_files(self, partial_results):
        results = []
        for filename, old_result in partial_results.items():
            with filename.open('r') as f:
                lines = f.read()
            for regex, col in self.file_regex.items():
                old_result[col] = regex.search(lines)
            results.append(old_result)
        return results
