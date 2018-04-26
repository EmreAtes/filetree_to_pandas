"""TreeParser class"""
from pathlib import Path

from parse import parse as pparse


class TreeParser:
    """Reads a given tree structure and returns a dataframe"""
    def __init__(self, directory_format=None):
        if directory_format:
            self.add_directory_format(directory_format)

    def add_directory_format(self, dir_format):
        """Defines the directory format of the parser

        Parameters
        ----------
        dir_format : string
            The format is provided similar to the python format strings.
            Directories are separated by the '/' character, {name} is used
            for names of the parameters. {} is used for irrelevant parameters.
        """
        self.dir_format = []
        for i, dirname in enumerate(dir_format.split('/')):
            self.dir_format[i] = dirname
        self.file_format = self.dir_format[-1]
        self.dir_format = self.dir_format[:-1]

    def parse(self, root_dir):
        """Parses the given root dir, returns the csv"""
        current_dir = Path(root_dir).expanduser()
        partial_results = {}
        partial_results[current_dir] = {}
        for cur_format in self.dir_format:
            partial_results = self._parse_dir(
                cur_format, partial_results)
        self._parse_files(self.file_format, partial_results)

    def _parse_dir(self, dir_format, partial_results):
        next_results = {}
        for current_dir, old_result in partial_results.items():
            for file_or_dir in current_dir.iterdir():
                cur_result = {
                    **old_result,
                    **pparse(nested_dir, file_or_dir)['named']
                }
                self.next_results[file_or_dir] = cur_result
        return next_results

    def _parse_files(self, file_format, partial_results):
        results = []
        for dirname, old_result in partial_results.items():
            for filename in dirname.iterdir():


