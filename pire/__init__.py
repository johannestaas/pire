'''
pire

Python Interactive Regular Expressions
'''
__title__ = 'pire'
__version__ = '0.0.1'
__all__ = ()
__author__ = 'Johan Nestaas <johannestaas@gmail.com'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2019 Johan Nestaas'

from .ui import run_pire


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--regex', '-r', default='regex.pire',
        help='path to text file with newline-delimited regular expressions',
    )
    parser.add_argument(
        'input_paths', nargs='+', help='paths to files to parse with regex',
    )
    args = parser.parse_args()
    run_pire(
        regex_path=args.regex,
        input_paths=args.input_paths,
    )
