import dataloads
import mergedocs
from datetime import datetime, timezone
import pymongo
import gc

client = pymongo.MongoClient("mongodb://localhost:27017/")
log_db = client["baseball"]       
log_collection = log_db['logs']



documents = [#{"route" : "sports", "response_path" : "sports"}#,
             #{"route" : "seasons", "response_path" : "seasons"},
             {"route" : "divisions","response_path" : "divisions" },
             {"route" : "leagues","response_path" : "leagues" },
             {"route" : "teams","response_path" : "teams"}#,
             #{"route" : "schedule", "response_path" : "dates"},
             #{"route" : "sports_players", "response_path" : "people"}
             ] 

current_year = datetime.now().year
run_start_time = datetime.now()

##Load single years
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
            logs.append({"jobId" : run_start_time,
                        "process" : "loadDocs", 
                         "document": i['route'], 
                         "start_time" : start_time.isoformat(), 
                         "end_time": end_time.isoformat(), 
                         "run_time" : str(run_time),
                         "document_count" : records } )
            
    log_collection.insert_many(logs)
    del(start_time, end_time, run_time, records, logs)

##Loads a range of years
def loaddocs_years(y: int) :
    logs = [] 
    for i in documents :
            start_time = datetime.now()
            print(f"{i["route"]} loading start at {start_time}")
            records = dataloads.MongoDBStageLoader(i['route'],y,i['response_path']).loadStageDocuments()
            end_time = datetime.now()
            run_time = end_time - start_time
            print(f"{i['route']} loading completed at {end_time} in {run_time} with {records} documents")
            #print(records)
            logs.append({"jobId" : run_start_time,
                        "process" : "loadDocs", 
                         "document": i['route'], 
                         "start_time" : start_time.isoformat(), 
                         "end_time": end_time.isoformat(), 
                         "run_time" : str(run_time),
                         "document_count" : records } )
            
    log_collection.insert_many(logs)
    del(start_time, end_time, run_time, records, logs)


def main() :
    ##loaddocs()
    for i in range(2000,2027) : 
         loaddocs_years(i)

if __name__ == "__main__" :
    main()