import os
import time

import boto3
from boto3.s3.transfer import S3Transfer
from django.conf import settings



# def s3_upload(file_):
#     """upload file in s3 bucket and generate a url"""
#
#     config_dict = {
#         "bucket": "todo_pic",
#         "region": "us-east-2"}
#
#     file_arr = file_.name.split(".")
#     file_name = file_arr[0] + "_" + str(int(time.time())) + "." + file_arr[1]
#     file_extension = file_arr[1]
#
#     # Saving file into my local machine(or server)
#     FILENAME = "/tmp/%s" % (file_name or "")
#     with open(FILENAME, "wb") as f:
#         f.write(file_.read())
#
#     media_extensions = ('jpeg','jpg', 'gif', 'png', 'svg', 'tiff')
#     folder_name = 'media' if file_extension in media_extensions else 'documents'
#
#     region = config_dict['region']
#     bucket = config_dict['bucket']
#     key = 'codeleap/%s/%s' % (folder_name, file_name)
#     credentials = {'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
#                    'aws_secret_access_key':settings.AWS_SECRET_ACCESS_KEY}
#     client = boto3.client('s3', region, **credentials)
#
#     transfer = S3Transfer(client)
#     transfer.upload_file(FILENAME, bucket, key, extra_args={'ACL': 'public-read'})
#
#     file_url = '%s/%s/%s' % (client.meta.endpoint_url, bucket, key)
#
#     return file_url
