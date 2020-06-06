import os

import boto3

### This is a bug in boto3
# os.environ["AWS_ACCESS_KEY_ID"] = "test"
# os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

region_name = "us-east-1"
# bucket_name = 'arn:aws:s3:::openaq-fetches/daily'
bucket_name = "openaq-fetches"

s3client = boto3.client("s3", region_name=region_name)
objects = s3client.list_objects_v2(Bucket=bucket_name)
