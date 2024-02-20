import os
from datetime import datetime

import boto3
from botocore.exceptions import ClientError


def backup_directory(directory: str, bucket_name: str, bucket_directory: str, s3_client=None) -> None:
    """
    Backs up the directory to the bucket.

    :param directory: The directory to back up.
    :param bucket_name: The name of the bucket to back up the directory to.
    :param bucket_directory: The name of the backed up directory in the bucket.
    :param s3_client: The S3 Client to use. A simple client will be created if none is specified.
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
            if should_backup(file_path, bucket_name, object_key, s3_client):
                print(f'Backing up {relative_file_path}...', end='')
                s3_client.upload_file(file_path, bucket_name, object_key)
                print(' completed.')
            else:
                print(f'Already backed up {relative_file_path}.')


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
