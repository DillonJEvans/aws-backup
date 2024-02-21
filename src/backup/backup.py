import os
import sys
from datetime import datetime
from typing import Callable, Optional

import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name: str, s3_client=None) -> bool:
    """
    Creates the bucket if possible.
    Prints a message if the bucket was created or if something goes wrong.

    :param bucket_name: The name of the bucket to create.
    :param s3_client: The S3 Client to use. A simple client will be created if none is specified.
    :return: True if the bucket exists after this function, False otherwise.
    """
    # Create a simple S3 Client if none was specified.
    if s3_client is None:
        s3_client = boto3.client('s3')
    # Check if the bucket already exists.
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        pass
    # Prepare to try to create the bucket.
    region = s3_client.meta.region_name
    bucket_config = {'LocationConstraint': region}
    # Try to create the bucket.
    print('Attempting to create the bucket...', end='')
    try:
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=bucket_config)
    except ClientError as e:
        # If creating the bucket failed, then print an error message and return False.
        error_code = e.response['Error']['Code']
        return print_create_bucket_error(error_code, bucket_name)
    # The bucket was successfully created.
    print(' success.')
    return True


def print_create_bucket_error(error_code: str, bucket_name: str) -> bool:
    """
    Prints an error for the create_bucket() function.

    :param error_code: The error code (ClientError['Error']['Code']) of the exception.
    :param bucket_name: The name of the bucket that was attempted to be created.
    :return: True if the bucket was created, False otherwise.
    """
    if error_code == 'BucketAlreadyOwnedByYou':
        print(' success.')
        return True
    print()
    if error_code == 'BucketAlreadyExists':
        error_message = f'"{bucket_name}" is owned by someone else. Please try again with a different bucket name.'
    elif error_code == 'InvalidBucketName':
        error_message = f'"{bucket_name}" is an invalid bucket name. Please try again with a different bucket name.'
    else:
        error_message = 'An unexpected error occurred while trying to create the bucket.'
    print(error_message, file=sys.stderr)
    return False


def backup_directory(directory: str, bucket_name: str, bucket_directory: str, s3_client=None,
                     callback: Optional[Callable[[str, bool], None]] = None) -> None:
    """
    Backs up the directory to the bucket.

    :param directory: The directory to back up.
    :param bucket_name: The name of the bucket to back up the directory to.
    :param bucket_directory: The name of the backed up directory in the bucket.
    :param s3_client: The S3 Client to use. A simple client will be created if none is specified.
    :param callback: An optional callback function that will be called after each file is backed up.
                     The parameters are the backed up file's path,
                     and whether the file was backed up or not.
    """
    # Create a simple S3 Client if none was specified.
    if s3_client is None:
        s3_client = boto3.client('s3')
    # Walk the directory, backing up every file that needs to be backed up.
    for path, directory_names, file_names in os.walk(directory):
        relative_path = get_relative_path(path, directory)
        for file_name in file_names:
            # Get the absolute path, relative path, and object key of the file.
            file_path = os.path.join(path, file_name)
            relative_file_path = os.path.join(relative_path, file_name)
            object_key = os.path.join(bucket_directory, relative_file_path)
            # Backup the file if needed.
            should_backup_file = should_backup(file_path, bucket_name, object_key, s3_client)
            if should_backup_file:
                print(f'Backing up         {relative_file_path}', end='')
                try:
                    s3_client.upload_file(file_path, bucket_name, object_key)
                    print()
                except ClientError:
                    print('    failed', file=sys.stderr)
                    should_backup_file = False
            else:
                print(f'Already backed up  {relative_file_path}')
            # Call the callback if there is one.
            if callback is not None:
                callback(file_path, should_backup_file)


def should_backup(file_path: str, bucket_name: str, object_key: str, s3_client=None) -> bool:
    """
    Determines if the file should be backed up.

    If the file has not been backed up (object_key is not present in the bucket) then it should be backed up.
    Otherwise, the file should be backed up if it has been modified more recently than the current backup.

    :param file_path: The file path on this machine.
    :param bucket_name: The name of the bucket.
    :param object_key: The expected name/key of the file/object in the bucket.
    :param s3_client: The S3 Client to use. A simple client will be created if none is specified.
    :return: True if the file should be backed up, false otherwise.
    """
    # Create a simple S3 Client if none was specified.
    if s3_client is None:
        s3_client = boto3.client('s3')
    # Get the last modified date of the backed up object.
    try:
        object_metadata = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        backup_last_modified = object_metadata['LastModified']
    except ClientError:
        # If the object_key could not be found, the file needs to be backed up.
        return True
    # Get the last modified date of the local file.
    local_timestamp = os.path.getmtime(file_path)
    local_last_modified = datetime.fromtimestamp(local_timestamp)
    local_last_modified = local_last_modified.astimezone()
    return local_last_modified > backup_last_modified


def get_relative_path(path: str, root: str = os.curdir) -> str:
    """
    Gets the relative path to path from root.
    The only difference between this function and os.path.relpath()
    is that this function returns an empty string when path and root are the same.

    :param path: The path.
    :param root: The root path.
    :return: The relative path to path from root.
    """
    if os.path.samefile(path, root):
        return ''
    return os.path.relpath(path, root)
