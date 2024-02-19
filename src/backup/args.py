import os
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from typing import Tuple


class Arguments:
    """Data class for storing command line arguments."""

    def __init__(self, args: Namespace) -> None:
        """
        Initializes the object from the Namespace object.
        :param args: The Namespace from ArgumentParser.parse_args().
        """
        self.source_dir: str = args.source
        self.bucket_name: str = args.destination[0]
        self.bucket_dir: str = args.destination[1]


def parse_arguments() -> Arguments:
    """
    Parses command line arguments.
    Exits the program if the arguments are invalid.
    :return: The parsed arguments.
    """
    parser = ArgumentParser(description='Makes a backup to AWS.')
    parser.add_argument('source', metavar='directory', type=directory, help='directory to backup')
    parser.add_argument('destination', metavar='bucket::directory', type=bucket_and_directory,
                        help='bucket and directory to backup to')
    return Arguments(parser.parse_args())


def directory(raw_path: str) -> str:
    """Meant to be used a type converter for ArgumentParser.add_argument()."""
    if not os.path.isdir(raw_path):
        raise ArgumentTypeError('no such directory')
    return raw_path


def bucket_and_directory(name: str) -> Tuple[str, str]:
    """Meant to be used a type converter for ArgumentParser.add_argument()."""
    elements = name.split('::')
    if len(elements) != 2:
        raise ArgumentTypeError('missing bucket directory')
    return elements[0], elements[1]
