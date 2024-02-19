from .args import parse_arguments

from ..utils.size import directory_size, format_size


def main():
    args = parse_arguments()
    print(args.source_dir)
    print(args.bucket_name)
    print(args.bucket_dir)
    size = directory_size(args.source_dir)
    print(f'{args.source_dir} is {size} bytes, or {format_size(size)}.')


if __name__ == '__main__':
    main()
