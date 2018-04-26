# treeparser
Read a tree structure into a pandas dataframe

The `TreeParser` class is provided by this package. It accepts two parameters,
`directory_format` and `file_regex`, which are both lists of regular expressions.
The groups that match in the regex are placed into the corresponding column in the
resulting dataframe.

## Usage
Assume we run multiple applications and place the results in directories with the
application names and inputs. E.g., `BT_X` is the directory where the output of the
application `BT` with the input `X` is stored.

In each directory there are files with the running time in them. The file name is
`1923_slurm.out` for job no. `1923`. The running time is identified with the line e.g.,
`Total time (s) = 25`

```
parser = TreeParser(
    directory_format=[
        r'(?P<app>[^_]*)_(?P<input>.*)',
        r'(?P<jobid>\d*)_slurm\.out'
    ], file_regex=[
        r'^Total time \(s\) = (?P<time>\d*)$',
    ])
df = parser.parse('~/location/to/root')
```
