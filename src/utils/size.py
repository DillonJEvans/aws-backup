import os
from math import floor
from typing import Tuple


# Constants for use as format_size() unit labels (the units parameter).
SIZES: Tuple[str, ...] = ('bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
SIZES_ABBRV: Tuple[str, ...] = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
TRANSMISSION_RATES: Tuple[str, ...] = ('bps', 'Kbps', 'Mbps', 'Gbps', 'Tbps', 'Pbps', 'Ebps', 'Zbps', 'Ybps')


def directory_size(directory: str, followlinks: bool = False) -> int:
    """
    Sums the size of all files in the directory and all subdirectories.
    :param directory: The directory to get the size of.
    :param followlinks: True to follow symbolic links, False otherwise.
    :return: The size of the directory in bytes.
    """
    size = 0
    for dirpath, dirnames, filenames in os.walk(directory, followlinks=followlinks):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if followlinks or not os.path.islink(full_path):
                size += os.path.getsize(full_path)
    return size


def format_size(size: int, units: Tuple[str, ...] = SIZES, unit_size: int = 1024):
    """
    Formats the given size (typically either in bytes or bits) to a human-readable string.

    The format of the size is inspired by how sizes are formatted
    in the Properties window in Windows File Explorer.
    Sizes are rounded to 3 significant figures, unless they fit within the smallest unit,
    in which case they are not rounded.

    Examples::

        format_size(1_023)     == '1,023 bytes'
        format_size(1_024)     == '1.00 KB'
        format_size(15_000)    == '14.6 KB'
        format_size(150_000)   == '146 KB'
        format_size(1_024_000) == '0.97 MB'

    :param size: The size, typically either in bits or bytes.
    :param units: The unit labels to use.
    :param unit_size: The size of a unit, typically either 1000 for decimal units or 1024 for binary units.
    :return: A human-readable string representing the given size.
    """
    # Don't round the smallest unit.
    if size < unit_size:
        return f'{size:,} {units[0]}'
    # Determine the unit to use without exceeding the largest unit.
    # Compares to 1000, not unit_size,
    # so that the ending value of size does not exceed 3 digits.
    unit = 0
    while size >= 1000 and unit + 1 < len(units):
        size /= unit_size
        unit += 1
    # Determine how many decimal places to display (round to 3 significant figures).
    decimal_places = 0
    if size < 10:
        decimal_places = 2
    elif size < 100:
        decimal_places = 1
    # Floor the size to 3 significant figures.
    # Specifying precision in the f-string would round it, not floor it.
    # Flooring is desired as it matches how windows displays file/directory sizes.
    size *= 10 ** decimal_places
    size = floor(size)
    size /= 10 ** decimal_places
    # Still include the precision in the f-string, just in case of rounding errors.
    return f'{size:,.{decimal_places}f} {units[unit]}'