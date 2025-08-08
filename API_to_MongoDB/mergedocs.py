import pymongo

class MongoDBMerger:
       
    def __init__(merge, document):
        # Connect to MongoDB
        merge.document = document
        merge.client = pymongo.MongoClient("mongodb://localhost:27017/")
        merge.stage_db = merge.client["stg_baseball"]
        merge.stage_doc = 'stg_' + document
        merge.stage_collection = merge.stage_db[merge.stage_doc]

    def merge(merge):
        merge.stage_collection.aggregate([
            {"$unset": "_id"},  # Remove _id field to avoid conflicts
            {"$merge": {
            "into": {"db": "baseball", "coll": merge.document},  # target data collection
            "on": "idx",
            "whenMatched": "replace",
            "whenNotMatched": "insert"
        }
    }])

obg = MongoDBMerger('sports')
obg.merge()