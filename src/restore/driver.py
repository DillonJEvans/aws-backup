import boto3

from .args import parse_arguments
from .restore import bucket_exists, restore_directory
from ..utils.progress import ProgressLogger
from ..utils.size import bucket_directory_summary, format_size


def main():
    args = parse_arguments()
    # Create a reusable client.
    s3_client = boto3.client('s3')
    if not bucket_exists(args.bucket_name):
        return
    # Prepare the progress logger and print a cool sounding message for the user to read.
    print('Calculating the size of the directory...')
    directory_info = bucket_directory_summary(args.bucket_name, args.bucket_dir, s3_client=s3_client)
    progress = ProgressLogger(directory_info.file_count, directory_info.total_size)
    formatted_directory_size = format_size(directory_info.total_size)
    print(f'Restoring {directory_info.file_count} files ({formatted_directory_size}).')
    progress.print_progress_info()
    # Begin the restoration.
    restore_directory(args.bucket_name, args.bucket_dir, args.destination_dir,
                      s3_client=s3_client, callback=progress.complete_file)
    print('\nRestoration completed.')


if __name__ == '__main__':
    main()
