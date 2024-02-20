import boto3

from .args import parse_arguments
from .backup import backup_directory
from ..utils.size import directory_summary, format_size


def main():
    args = parse_arguments()
    dir_info = directory_summary(args.source_dir)
    print(
        f'{args.source_dir} has {dir_info.directory_count} directories, '
        f'{dir_info.file_count} files and is {format_size(dir_info.total_size)}'
        f'{f" ({dir_info.total_size:,} bytes)" if dir_info.total_size >= 1024 else ""}.'
    )
    backup_directory(args.source_dir, args.bucket_name, args.bucket_dir)


if __name__ == '__main__':
    main()
