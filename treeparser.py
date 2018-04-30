"""TreeParser class"""
from pathlib import Path
import re

import pandas as pd


class TreeParser:
    """Reads a given tree structure and returns a dataframe"""
    def __init__(self, directory_format=None, file_regex=None):
        """Defines the directory and file format of the parser

        Parameters
        ----------
        directory_format : List[regex]
            The format is a list of regular expressions. The names of the
            fields are given by named groups: `(?P<name>...)` other groups are
            discarded. Each list element corresponds to a directory level, and
            the last one is the file name format.
            Any directory or file that doesn't match the format is ignored.
        file_regex : List[regex]
            regex is searched for in each file, and the result of the match is
            placed in the column with the corresponding group name.
        """
        self.dir_format = directory_format
        self.file_regex = [re.compile(p, flags=re.MULTILINE)
                           for p in file_regex]

    def parse(self, root_dir):
        """Parses the given root dir, returns the csv"""
        current_dir = Path(root_dir).expanduser()
        partial_results = {}
        partial_results[current_dir] = {}
        for cur_format in self.dir_format:
            partial_results = self._parse_dir(
                cur_format, partial_results)
        results = self._parse_files(partial_results)
        return pd.DataFrame(results)

    def _parse_dir(self, dir_format, partial_results):
        next_results = {}
        for current_dir, old_result in partial_results.items():
            for file_or_dir in current_dir.iterdir():
                res = re.match(dir_format, file_or_dir.name)
                if res is None:
                    print(f"Regex {dir_format} failed for file {file_or_dir}")
                    continue
                next_results[file_or_dir] = {**old_result, **res.groupdict()}
        return next_results

    def _parse_files(self, partial_results):
        results = []
        for filename, old_result in partial_results.items():
            with filename.open('r') as f:
                lines = f.read()
            for regex in self.file_regex:
                res = regex.search(lines)
                if res is None:
                    print(f"Regex {regex} failed for file {filename}")
                old_result = {**old_result, **res.groupdict()}
            results.append(old_result)
        return results
