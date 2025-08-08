import dataloads
import mergedocs
from datetime import datetime, timezone
import pymongo
import gc

client = pymongo.MongoClient("mongodb://localhost:27017/")
log_db = client["baseball"]       
log_collection = log_db['logs']



documents = [{"route" : "sports", "response_path" : "sports"},
             {"route" : "seasons", "response_path" : "seasons"},
             {"route" : "divisions","response_path" : "divisions" },
             {"route" : "leagues","response_path" : "leagues" },
             {"route" : "teams","response_path" : "teams"}] 

current_year = datetime.now().year

def loaddocs() :
    logs = [] 
    for i in documents :
            start_time = datetime.now()
            print(f"{i["route"]} loading start at {start_time}")
            records = dataloads.MongoDBStageLoader(i['route'],current_year,i['response_path']).loadStageDocuments()
            end_time = datetime.now()
            run_time = end_time - start_time
            print(f"{i['route']} loading completed at {end_time} in {run_time} with {records} documents")
            #print(records)
            logs.append({"process" : "loadDocs", 
                         "document": i['route'], 
                         "start_time" : start_time.isoformat(), 
                         "end_time": end_time.isoformat(), 
                         "run_time" : str(run_time),
                         "document_count" : records } )
            
    log_collection.insert_many(logs)
    del(start_time, end_time, run_time, records, logs)


def main() :
    loaddocs()

if __name__ == "__main__" :
    main()