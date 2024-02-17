from argparse import ArgumentParser, ArgumentError, ArgumentTypeError
from os import path
from typing import Tuple


def parse_arguments():
    parser = ArgumentParser(description='Makes a backup to AWS.')
    parser.add_argument('source', metavar='directory', type=directory, help='directory to backup')
    parser.add_argument('destination', metavar='bucket::directory', type=bucket_and_directory, help='bucket and directory to backup to')
    return parser.parse_args()


def directory(raw_path: str) -> str:
    if path.isdir(raw_path):
        return raw_path
    else:
        raise ArgumentTypeError(f'no such file or directory: {raw_path}')


def bucket_and_directory(name: str) -> Tuple[str, str]:
    elements = name.split('::')
    if len(elements) != 2:
        raise ArgumentError()
    return elements[0], elements[1]
