import os
import boto3
from io import StringIO
import pandas as pd

# set environment variable
BUCKET_NAME = os.environ['BUCKET_NAME']
FILE_NAME = os.environ['FILE_NAME']

# Create S3 object
s3_resource = boto3.resource("s3")

class MissingFileError(Exception):
    def __init__(self, key: str, message: str = "File Not Found"):
        self.key = key
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message}: {self.key}"

def retrieve_from_data_bucket(bucket_arg: str):
    try:
        s3_to_dataframe = pd.read_csv(
            s3_resource.Object(BUCKET_NAME, bucket_arg).get().get("Body"),
            index_col="date",
            parse_dates=True,
        )
        return s3_to_dataframe
    except s3_resource.meta.client.exceptions.NoSuchKey:
        raise MissingFileError(bucket_arg)


def save_data_to_s3(last_saved_data: pd.DataFrame):
    
    """ Write a dataframe to a CSV on S3 """
    print("Writing {} records to {}".format(len(last_saved_data), FILE_NAME))
    # Create buffer
    csv_buffer = StringIO()
    # Write dataframe to buffer
    last_saved_data.to_csv(csv_buffer)
    # Create S3 object
    s3_resource = boto3.resource("s3")
    # Write buffer to S3 object
    s3_resource.Object(BUCKET_NAME, FILE_NAME).put(Body=csv_buffer.getvalue())