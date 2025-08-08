##from pymongo import MongoClient
import pymongo


# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

documents = ['schedule',]


def add_data_index(document: str) :
    # Set MongoDB database and collection
    db = client["baseball"]
    collection = db[document]

    # Merge stage collection into base collection
    collection.create_index([('idx', pymongo.ASCENDING)], unique=True)

def add_stage_index(document: str) :
    # Set MongoDB database and collection
    db = client["stg_baseball"]
    stg_doc = 'stg_' + document
    collection = db[stg_doc]

    # Merge stage collection into base collection
    collection.create_index([('idx', pymongo.ASCENDING)], unique=True)


add_data_index('schedule')
add_stage_index('schedule')


