import os
import shutil
import uuid
import logging
import boto3
import json

logger = logging.getLogger()

class TeeTimes:
    S3_BUCKET = "tee-times"

    def __init__(self, results, key):
        self.results = results
        self.s3_key = key

    def upload(self):
        s3 = boto3.resource('s3')
        obj = s3.Object(self.S3_BUCKET, self.s3_key)
        obj.put(Body=json.dumps(self.results))
        logger.info('Uploaded to S3: {}'.format(self.s3_key))
