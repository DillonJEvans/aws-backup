import os
import sys
from typing import Callable, Optional

import boto3
from botocore.exceptions import ClientError


def bucket_exists(bucket_name: str, s3_client=None) -> bool:
    """
    Checks if the bucket exists.

    :param bucket_name: The name of the bucket.
    :param s3_client: The S3 Client to use. A simple client will be created if none is specified.
    :return: True if the bucket exists, False otherwise.
    """
    # Create a simple S3 Client if none was specified.
    if s3_client is None:
        s3_client = boto3.client('s3')
    # If head_bucket() works, then the bucket exists, otherwise the bucket does not exist.
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        pass
    return False


def restore_directory(bucket_name: str, bucket_directory: str, directory: str, s3_client=None,
                      callback: Optional[Callable[[str, bool], None]] = None) -> None:
    """
    Restores the directory from the bucket.

    :param bucket_name: The name of the bucket the directory to restore from is in.
    :param bucket_directory: The name of the directory to restore from.
    :param directory: The directory to restore to.
    :param s3_client: The S3 Client to use. A simple client will be created if none is specified.
    :param callback: An optional callback function that will be called after each file is restored.
                     The parameters are the restored file's path,
                     and whether the file was restored or not.
    """
    # Create a simple S3 Client if none was specified.
    if s3_client is None:
        s3_client = boto3.client('s3')
    # Use a paginator to get the list of all objects in the bucket and directory.
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=bucket_directory)
    # Iterate over all the returned objects.
    for page in page_iterator:
        for bucket_object in page.get('Contents', []):
            # Get the object key, relative path, and absolute path of the file.
            object_key = bucket_object['Key']
            relative_file_path = os.path.relpath(object_key, bucket_directory)
            file_path = os.path.join(directory, relative_file_path)
            create_parent_directories(file_path)
            # Restore the file.
            print(f'Restoring  {relative_file_path}', end='')
            try:
                s3_client.download_file(bucket_name, object_key, file_path)
                restored = True
                print()
            except ClientError:
                restored = False
                print('    failed', file=sys.stderr)
            # Call the callback if there is one.
            if callback is not None:
                callback(file_path, restored)


def create_parent_directories(file_path: str) -> None:
    """
    Creates the directories containing the file_path,
    if they don't already exist.
    :param file_path: The path to the file.
    """
    parent_directories = os.path.dirname(file_path)
    if not os.path.exists(parent_directories):
        os.makedirs(parent_directories)
