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

from .preprocessor import _preprocess


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--preprocess', '-p',
        help='',
    )
    parser.add_argument(
        '--regex', '-r',
        default='regex.pire',
        help='',
    )
    parser.add_argument('input_file')
    args = parser.parse_args()
    if args.preprocess:
        preprocess = _preprocess(args.preprocess)
    else:
        def preprocess(f):
            yield from f
    with open(args.input_file) as f:
        for line in preprocess(f):
            print('parsed line')
