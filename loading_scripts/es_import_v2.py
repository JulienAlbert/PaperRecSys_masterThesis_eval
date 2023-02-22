import json
from tqdm import tqdm
from elasticsearch import Elasticsearch, helpers
import time

DATASET_PATH = 'dblp.v12.json'
PAPER_CIT_DICT_PATH = 'paper_cit_dict.json'
N_RECORDS = 4894081
INDEX_NAME = 'dblp_v12'

es = Elasticsearch([{'host':'localhost', 'port':9200}])

# suppress index if already created
try:
    es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    print('index deleted')
except:
    print('no index')
    
# load paper citations dict
with open(PAPER_CIT_DICT_PATH) as file:
    paper_cit_dict = json.load(file)
print('paper citations dict loaded')

# create new index
settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,        
            "similarity": {
                "scripted_tfidf": {
                    "type": "scripted",
                    "script": {
                        "source": "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "similarity": "scripted_tfidf"
                    },
                "abstract": {
                    "type": "text",
                    "similarity": "scripted_tfidf"
                }
            }
        }
}
es.indices.create(index=INDEX_NAME, ignore=[400, 404], body=settings)
print('index created')

# import papers
def reconstruct_abstract(inverted_index):    
    index = {}
    for word, list_of_pos in inverted_index.items():
        for pos in list_of_pos:
            index[pos] = word
    
    abstract_list = []
    for _, word in sorted(index.items(), key=lambda t: t[0]):
        abstract_list.append(word)
    
    return " ".join(abstract_list)

with open(DATASET_PATH) as file:
    bulk = []
    file.readline() # skip first line
    
    for _ in tqdm(range(N_RECORDS)):
        line = file.readline()
        try:
            paper = json.loads(line[1:])
        except:
            paper = json.loads(line)
            
        formatted_paper = {} 
        formatted_paper['paper_id'] = paper['id']
        formatted_paper['title'] = paper['title']

        if 'indexed_abstract' in paper:
            indexed_abstract = paper.pop('indexed_abstract')
            formatted_paper['abstract'] = reconstruct_abstract(indexed_abstract['InvertedIndex'])
        else:
            formatted_paper['abstract'] = ''
            
        if 'fos' in paper:
            formatted_paper['fos'] = [fos['name'].lower() for fos in paper['fos']]
        else:
            formatted_paper['fos'] = []
            
        formatted_paper['doi'] = paper.pop('doi', '')
        
        linked_papers = []
        if 'references' in paper:
            linked_papers = paper['references']
        if paper['id'] in paper_cit_dict:
            linked_papers += paper_cit_dict[paper['id']]
        formatted_paper['linked_papers'] = linked_papers
            
        bulk.append(formatted_paper)

        if len(bulk) > 1000:
            try:
                helpers.bulk(es, bulk, index=INDEX_NAME)
                bulk = []
            except:
                print('bulk error, wait 60s then retry')
                time.sleep(60)
                helpers.bulk(es, bulk, index=INDEX_NAME)
                bulk = []
                
    if bulk:
        try:
            helpers.bulk(es, bulk, index=INDEX_NAME)
        except:
            print('bulk error, wait 60s then retry')
            time.sleep(60)
            helpers.bulk(es, bulk, index=INDEX_NAME)

es.indices.refresh(INDEX_NAME)
result = es.cat.count(INDEX_NAME, params={"format": "json"})
print('papers importted', str(result))
