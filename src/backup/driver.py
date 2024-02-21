import boto3

from .args import parse_arguments
from .backup import backup_directory, create_bucket
from ..utils.progress import ProgressLogger
from ..utils.size import directory_summary, format_size


def main():
    args = parse_arguments()
    # Create the reusable client and the bucket.
    s3_client = boto3.client('s3')
    if not create_bucket(args.bucket_name, s3_client):
        return
    # Prepare the progress logger and print a cool sounding message for the user to read.
    print('Calculating the size of the directory...', end='')
    directory_info = directory_summary(args.source_dir)
    progress = ProgressLogger(directory_info.file_count, directory_info.total_size)
    formatted_directory_size = format_size(directory_info.total_size)
    print(f' backing up {directory_info.file_count} files ({formatted_directory_size}).')
    progress.print_progress_info()
    # Begin the backup.
    backup_directory(args.source_dir, args.bucket_name, args.bucket_dir,
                     s3_client=s3_client, callback=progress.complete_file)
    print('\nBackup completed.')


if __name__ == '__main__':
    main()
