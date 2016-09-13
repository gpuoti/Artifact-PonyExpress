"""
Here are grouped some useful functions to prepare test cases.
"""

import os
import os.path
import errno
import pymongo

def ensure_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
            
def touch(file_path):
    with open(file_path, 'w') as f:
        f.write(file_path)

def files_in(folder='.'):
    return [name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))]

def subfolders_in(folder='.'):
    return [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

class MongoChecker:
    def __init__(self, host='localhost', port=27017):
        # establish mongo connection and retrieve the broker_store collection
        self.connection = pymongo.MongoClient(host, port)
        self.collection = self.connection.broker_store.packages


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def contain(self, mongo_query, n=1):
        results = self.collection.find(mongo_query)
        try:
            return len(results[0]) >= n
        except IndexError:
            pass
        return False

class WorkingDirectorySet:
    def __init__ (self, folder):
        self.restore_to = os.getcwd()
        self.requested_folder = folder

    def __enter__(self):
        os.chdir(self.requested_folder)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.restore_to)

    def __str__(self):
        return self.requested_folder

def mongo_clean(host='localhost', port=27017):
    # establish mongo connection and retrieve the broker_store collection
    connection = pymongo.MongoClient(host, port)
    collection = connection.broker_store.packages

    collection.delete_many({"TEST": ""})
    connection.close()