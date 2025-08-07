import pymongo
import gc
import requests
import mergedocs 

class MongoDBStageLoader():
    def __init__(loader,document,year, response_path ) :
        loader.document = document
        loader.year = year
        loader.client = pymongo.MongoClient("mongodb://localhost:27017/")
        loader.response_path = response_path
        loader.stage_db = loader.client["stg_baseball"]       
        loader.stage_doc = 'stg_'+ document
        loader.temp_doc = 'temp_'+ document
        loader.stage_collection = loader.stage_db[loader.stage_doc]
        loader.temp_collection = loader.stage_db[loader.temp_doc]
        loader.prod_db = loader.client["baseball"]
        loader.prod_collection = loader.prod_db["sports"]
        loader.sports = loader.prod_collection.find({},{"id" : 1, "year" :1, "_id" : 0})


    def api_call(loader, url:str) :
        response = requests.get(url)
        json_data = response.json()
                    
        # Clean up the response to free memory
        del response
        gc.collect()
        return json_data
    
    def getSports(loader,year,response_path) :
        url = f'http://statsapi.mlb.com/api/v1/sports?season={year}'      
        json_data = loader.api_call(url)
                
        if response_path in json_data :
            d = json_data[response_path]
            del json_data
            gc.collect

            if d != [] :
                loader.temp_collection.drop()
                loader.temp_collection.insert_many(d)
                loader.temp_collection.update_many({},[{"$set": {"year" : year, "idx" : {"$concat": ["I", 
                                                {"$toString": "$id"},
                                                'Y',
                                                {"$toString" : year}]}}}])
                
                loader.temp_collection.aggregate([
                     {"$unset": ("_id")},  # Remove _id field to avoid conflicts
                     {"$merge": {
                     "into": {"db": "stg_baseball", "coll": loader.stage_doc},  # target data collection
                     "on": "idx",
                     "whenMatched": "replace",
                     "whenNotMatched": "insert"
                       }
                      }])
                
                loader.temp_collection.drop()
                mergedocs.MongoDBMerger(loader.document)
                del (d)
                gc.collect()

    def getSeasons(loader) :
        for i in loader.sports :
            sport_id = i["id"]
            yr = i["year"]
            url = f'http://statsapi.mlb.com/api/v1/seasons?sportId={sport_id}&season={yr}'
            json_data = loader.api_call(url)
                
            if loader.response_path in json_data :
                d = json_data[loader.response_path]
                del json_data
                gc.collect

                if d != [] :
                    loader.temp_collection.drop()
                    loader.temp_collection.insert_many(d)
                    loader.temp_collection.update_many({},[{"$set": {"sportId" : sport_id, "year" : yr,  "idx" : {"$concat": ["I", 
                                            {"$toString": "$seasonId"},
                                            "S",
                                            {"$toString" : sport_id},
                                            'Y',
                                            {"$toString" : yr}]}}}])
                
                    loader.temp_collection.aggregate([
                    {"$unset": ("_id")},  # Remove _id field to avoid conflicts
                    {"$merge": {
                    "into": {"db": "stg_baseball", "coll": loader.stage_doc},  # target data collection
                    "on": "idx",
                    "whenMatched": "replace",
                    "whenNotMatched": "insert"
                    }}])
                
                    loader.temp_collection.drop()
                    del(d)
                    gc.collect

    def getRoots(loader) :
        sport_id = [i for i in loader.sports if i["year"] == loader.year]
        for i in sport_id :
            s_id = i["id"]
            
            if s_id :
                url = f'https://statsapi.mlb.com/api/v1/{loader.document}?sportId={s_id}&season={loader.year}'
                json_data = loader.api_call(url)
                
                if  loader.response_path in json_data :
                    d = json_data[loader.response_path]
                    del json_data
                    gc.collect

                    if d != [] :
                        loader.temp_collection.drop()
                        loader.temp_collection.insert_many(d)
                        loader.temp_collection.update_many({},[{"$set": {"sportId" : s_id, "year" : loader.year, 
                                             "idx" : {"$concat": ["I", 
                                            {"$toString": "$id"},
                                            "S",
                                            {"$toString" : s_id},
                                            'Y',
                                            {"$toString" : loader.year}]}}}])
                        
                                               
                        loader.temp_collection.aggregate([
                            {"$unset": ("_id")},  # Remove _id field to avoid conflicts
                            {"$merge": {
                            "into": {"db": "stg_baseball", "coll": loader.stage_doc},  # target data collection
                            "on": "idx",
                            "whenMatched": "replace",
                            "whenNotMatched": "insert"
                            }
                            }])
                
                        loader.temp_collection.drop()
                        mergedocs.MongoDBMerger(loader.document)
                        del (d)
                        gc.collect()

    
    
    def loadStageDocuments(loader) :
        if loader.document in ("conferences", "divisions", "leagues", "teams") :
            print(f"Loading {loader.document}")
            loader.getRoots()
            print(f"{loader.document} loading completed")

#obj = MongoDBStageLoader('leagues',2025,'leagues')
#obj.loadStageDocuments()


