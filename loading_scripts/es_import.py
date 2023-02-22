import json
from tqdm import tqdm
from elasticsearch import Elasticsearch, helpers
import time

es = Elasticsearch([{'host':'localhost', 'port':9200}])

# suppress index if already created
try:
    es.indices.delete(index='dblp_v12', ignore=[400, 404])
    print('index deleted')
except:
    print('no index')

# create new index
settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
}
es.indices.create(index='dblp_v12', ignore=[400, 404], body=settings)
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

dataset_path = 'dblp.v12.json'

with open(dataset_path) as file:
    bulk = []
    file.readline() # skip first line
    
    for _ in tqdm(range(4894081)): # n_papers
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
            formatted_paper['fos'] = ", ".join([fos['name'] for fos in paper['fos']])
        else:
            formatted_paper['fos'] = ''
            
        formatted_paper['doi'] = paper.pop('doi', '')
            
        bulk.append(formatted_paper)

        if len(bulk) > 1000:
            try:
                helpers.bulk(es, bulk, index='dblp_v12', doc_type='paper')
                bulk = []
            except:
                print('bulk error, wait 60s then retry')
                time.sleep(60)
                helpers.bulk(es, bulk, index='dblp_v12', doc_type='paper')
                bulk = []
                
    if bulk:
        helpers.bulk(es, bulk, index='dblp_v12', doc_type='paper')

es.indices.refresh('dblp_v12')
result = es.cat.count('dblp_v12', params={"format": "json"})
print('papers importted', str(result))
