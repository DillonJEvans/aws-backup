import boto3

from .args import parse_arguments
from .backup import backup_directory, create_bucket
# from ..utils.size import directory_summary, format_size


def main():
    args = parse_arguments()
    s3_client = boto3.client('s3')
    if not create_bucket(args.bucket_name, s3_client):
        return
    backup_directory(args.source_dir, args.bucket_name, args.bucket_dir, s3_client)


if __name__ == '__main__':
    main()
