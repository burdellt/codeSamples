import pymongo
import gc
import requests
import mergedocs 
from datetime import datetime

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
    
    def getSports(loader) :
        #loader.stage_collection.delete_many({})
        records = 0
        url = f'http://statsapi.mlb.com/api/v1/sports?season={loader.year}'      
        json_data = loader.api_call(url)
                
        if loader.response_path in json_data :
            d = json_data[loader.response_path]
            del json_data
            gc.collect

            if d != [] :
                records += len(d)
                loader.temp_collection.drop()
                loader.temp_collection.insert_many(d)
                loader.temp_collection.update_many({},[{"$set": {"year" : loader.year, "idx" : {"$concat": ["I", 
                                                {"$toString": "$id"},
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
        return(records)

    def getSeasons(loader) :
        #loader.stage_collection.delete_many({})
        records = 0
        sport_id = [i for i in loader.sports if i["year"] == loader.year]
        for i in sport_id :
            s_id = i["id"]
            url = f'http://statsapi.mlb.com/api/v1/seasons?sportId={s_id}&season={loader.year}'
            json_data = loader.api_call(url)
                
            if loader.response_path in json_data :
                d = json_data[loader.response_path]
                del json_data
                gc.collect

                if d != [] :
                    records += len(d)
                    loader.temp_collection.drop()
                    loader.temp_collection.insert_many(d)
                    loader.temp_collection.update_many({},[{"$set": {"sportId" : sport_id, "year" : loader.year,  "idx" : {"$concat": ["I", 
                                            {"$toString": "$seasonId"},
                                            "S",
                                            {"$toString" : sport_id},
                                            'Y',
                                            {"$toString" : loader.year}]}}}])
                
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
        return (records)

    
    def getSchedules(loader) :
        ##loader.stage_collection.delete_many({})
        records = 0
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
                        records += len(d)
                        loader.temp_collection.drop()
                        loader.temp_collection.insert_many(d)
                        
                        loader.temp_collection.update_many({},[{"$set": {"sportId" : s_id
                                            , "year" : loader.year, 
                                             "idx" : {"$concat": ["I", 
                                            "$date",
                                            "S",
                                            {"$toString" : s_id},
                                            'Y',
                                            {"$toString" : loader.year}
                                            ]}}}])
                        
                                               
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
        return (records)          

    
    def getSportsPlayers(loader) : 
        records = 0
        sport_id = [i for i in loader.sports if i["year"] == loader.year]
        for i in sport_id :
            s_id = i["id"]
            
            if s_id :
                url = f'https://statsapi.mlb.com/api/v1/sports/{s_id}/players?season={loader.year}'
                json_data = loader.api_call(url)
                
                if  loader.response_path in json_data :
                    d = json_data[loader.response_path]
                    del json_data
                    gc.collect
                    
                    
                    if d != [] :
                        records += len(d)
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
        return (records)

    def getRoots(loader) :
        ##loader.stage_collection.delete_many({})
        records = 0
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
                        records += len(d)
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
        return (records)          

    
    def loadStageDocuments(loader) :
        if loader.document in ("divisions", "leagues", "teams") :
            records = loader.getRoots()
            return(records)
        
        elif loader.document == 'seasons' :
            records = loader.getSeasons()
            return(records)
        
        elif loader.document == 'schedule' :
            records = loader.getSchedules()
            return(records)
        
        elif loader.document == 'sports_players' :
            records = loader.getSportsPlayers()
            return(records)

        elif loader.document == 'sports' :
            records = loader.getSports()
            return(records)
        
        else :
            print('unknown end point')




