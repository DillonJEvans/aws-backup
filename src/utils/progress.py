import os
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from .size import format_size, SIZES_ALIGNED_ABBRV


class ProgressLogger:
    """Logs progress made on backing up or restoring files."""

    completed_files: int
    total_files: int
    completed_size: int
    total_size: int
    trailing_spaces: int
    progress_bar_width: int
    progress_bar_complete: str
    progress_bar_incomplete: str

    def __init__(self, total_files=0, total_size=0, trailing_spaces=8,
                 progress_bar_width=20, progress_bar_complete='#', progress_bar_incomplete='.'):
        """
        Initializes the ProgressLogger.

        :param total_files: The total number of files.
        :param total_size: The total size of all files in bytes.
        :param trailing_spaces: The number of spaces to print after logging progress.
        :param progress_bar_width: The width of the progress bar (in characters).
        :param progress_bar_complete: The symbol for the complete part of the progress bar.
        :param progress_bar_incomplete: The symbol for the incomplete part of the progress bar.
        """
        self.completed_files = 0
        self.total_files = total_files
        self.completed_size = 0
        self.total_size = total_size
        self.trailing_spaces = trailing_spaces
        self.progress_bar_width = progress_bar_width
        self.progress_bar_complete = progress_bar_complete
        self.progress_bar_incomplete = progress_bar_incomplete

    def get_progress_info(self) -> str:
        """
        Creates a string representing the current progress, including:

        * Completion percentage
        * Progress bar
        * Completed Size / Total Size
        * Completed Files / Total Files

        :return: A string representing the current progress.
        """
        # Get the progress percentage and bar.
        progress = self.completed_size / self.total_size
        progress_percentage = f'{progress:>4.0%}'
        progress_bar = get_progress_bar(progress,
                                        width=self.progress_bar_width,
                                        complete=self.progress_bar_complete,
                                        incomplete=self.progress_bar_incomplete)
        # Get the progress in terms of size.
        formatted_size_complete = format_size(self.completed_size, units=SIZES_ALIGNED_ABBRV)
        formatted_size_total = format_size(self.total_size, units=SIZES_ALIGNED_ABBRV)
        # Ensure that any size between 0 and total_size will align properly.
        formatted_max_bytes = format_size(1000, units=SIZES_ALIGNED_ABBRV)
        max_size_len = max(map(len, (formatted_size_total, formatted_max_bytes)))
        size_progress = f'{formatted_size_complete:>{max_size_len}}/{formatted_size_total}'
        # Get the progress in terms of files.
        max_files_len = len(str(self.total_files))
        files_progress = f'{self.completed_files:>{max_files_len}}/{self.total_files} files'
        # Put everything together.
        return f'{progress_percentage} |{progress_bar}|  {size_progress}    {files_progress}'

    def print_progress_info(self, trailing_spaces: Optional[int] = None) -> None:
        """
        Prints the result from get_progress_info() with trailing spaces.

        :param trailing_spaces: The number of trailing spaces to print.
                                If trailing_spaces is None, the member variable is used instead.
        """
        if trailing_spaces is None:
            trailing_spaces = self.trailing_spaces
        print(f'{self.get_progress_info()}{" " * trailing_spaces}', end='')

    def complete_file(self, file_path: str, was_updated: bool) -> None:
        """
        Complete the given file, updating completed_files and completed_size,
        then calling print_progress_info().

        Meant to be used as a callback() function.

        :param file_path: The file to complete.
        :param was_updated: Whether the local or backup were updated. Not used for now.
        """
        self.completed_files += 1
        self.completed_size += os.path.getsize(file_path)
        self.print_progress_info()


def get_progress_bar(progress: float, width: int = 10, complete: str = '#', incomplete: str = '.') -> str:
    """
    Produces a text representation of a progress bar.

    :param progress: The progress percentage between 0 and 1 inclusive.
    :param width: The width of the progress bar (in characters).
    :param complete: The symbol for the complete part of the progress bar.
    :param incomplete: The symbol for the incomplete part of the progress bar.
    :return: A text representation of a progress bar.
    """
    # Uses Decimal to round half up (e.g. 0.5 -> 1, 1.5 -> 2)
    # rather than round() which rounds half to even (e.g. 0.5 -> 0, 1.5 -> 2)
    # https://stackoverflow.com/a/33019948
    complete_decimal = Decimal(progress * width)
    complete_decimal = complete_decimal.to_integral_value(rounding=ROUND_HALF_UP)
    complete_length = int(complete_decimal)
    incomplete_length = width - complete_length
    return complete * complete_length + incomplete * incomplete_length
