import boto3
from boto3 import s3
# connect to our S3 endpoint
resource = boto3.resource('s3',
endpoint_url = 'https://storage.ecmwf.europeanweather.cloud',
aws_access_key_id='X9G47J53UC3QAAYWZ1OZ',
aws_secret_access_key='8a2Yt6wuxdAKLo6erLIws3ni9f0xQ83de1jNxwap')

# connect to S3 bucket
bucket = resource.Bucket('openaq')
# list all the objects
for o in bucket.objects.all():
    print(o)
# download a file
bucket.upload_file(Key="test.h5", Filename="aaa.h5")
# upload a file
bucket.download_file(Key="2018.h5", Filename="aaa.h5")
# read an object 
obj = s3.Object(bucketname, itemname)
body = obj.get()['Body'].read()