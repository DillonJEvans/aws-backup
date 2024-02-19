from .args import parse_arguments

from ..utils.size import directory_summary, format_size


def main():
    args = parse_arguments()
    print(args.source_dir)
    print(args.bucket_name)
    print(args.bucket_dir)
    dir_info = directory_summary(args.source_dir)
    print(
        f'{args.source_dir} has {dir_info.count} files and is {format_size(dir_info.size)}'
        f'{f" ({dir_info.size:,} bytes)" if dir_info.size >= 1024 else ""}.'
    )


if __name__ == '__main__':
    main()
