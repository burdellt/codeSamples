import dataloads
import mergedocs
from datetime import datetime

documents = [{"route":"conferences", "response_path": "conferences"},
             {"route" : "divisions","response_path": "divisions" },
             {"route":"leagues","response_path": "leagues" },
             {"route":"teams","response_path": "teams"}] 

#dl = 
#md = mergedocs.

current_year = datetime.now().year
def loaddocs() : 
    for i in documents :
        
        dataloads.MongoDBStageLoader(i['route'],current_year,i['response_path']).loadStageDocuments()


def main() :
    loaddocs()

if __name__ == "__main__":
    main()