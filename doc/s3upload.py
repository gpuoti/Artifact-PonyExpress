import boto
import boto.s3
import sys
import os
from boto.s3.key import Key

class PublishOp(object):
    def __init__(self, source_file, destination):
        self.source = source_file
        self.s3_bucket = destination.replace('\\','/') 

def percent_cb(complete, total):
    print(str(complete/1024) + ' / ' + str(total/1024) + ' kb  transmitted')
    

def ls(base_path):
    ls_list = []
    files_to_publish = []
    for root, dirs, files in os.walk(base_path):
         files_to_publish += [os.path.join(root, f) for f in files]

    return [ PublishOp(file_path, file_path[len(base_path)+1:]) for file_path in files_to_publish ]

def publish(publish_ops, bucket_name):
    AWS_ACCESS_KEY_ID = 'AKIAJZYRYFD3OXP5UJFA'
    AWS_SECRET_ACCESS_KEY = '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'

    
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


    bucket = conn.get_bucket(bucket_name)

    for op in publish_ops:
        print 'Uploading %s to Amazon S3 bucket %s' % (op.source, op.s3_bucket)
        k = Key(bucket)
        k.key = op.s3_bucket
        k.set_contents_from_filename(op.source, cb=percent_cb, num_cb=5)

if __name__ == '__main__':
    publish(ls('user-doc/html'), bucket_name = 'artifact-pony-express')