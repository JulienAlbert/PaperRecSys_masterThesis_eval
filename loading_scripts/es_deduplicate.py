# inspire from : https://www.elastic.co/fr/blog/how-to-find-and-remove-duplicate-documents-in-elasticsearch

from elasticsearch import Elasticsearch
from tqdm import tqdm
import time

es = Elasticsearch([{'host':'localhost', 'port':9200}])
duplicate_docs_dict = {}

def populate_duplicate_docs_dict(hits):
    for item in hits:
        paper_id = item['_source']['paper_id']
        item_id = item['_id']

        duplicate_docs_dict.setdefault(paper_id, []).append(item_id)

# scroll over all docs
print('scroll over all docs')

data = es.search(index='dblp_v12', scroll='5s', body={"query": {"match_all": {}}})

scroll_id = data['_scroll_id']
scroll_size = len(data['hits']['hits'])

populate_duplicate_docs_dict(data['hits']['hits'])

pbar = tqdm()

while scroll_size > 0:
    try:
        data = es.scroll(scroll_id=scroll_id, scroll='5s')
    except:
        time.sleep(60)
        data = es.scroll(scroll_id=scroll_id, scroll='5s')
    
    populate_duplicate_docs_dict(data['hits']['hits'])

    scroll_id = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])

    pbar.update(1)

pbar.close()

# remove duplicates
print('remove duplicates')

duplicates = [(paper_id, item_ids) for (paper_id, item_ids) in duplicate_docs_dict.items() if len(item_ids) > 1]

for paper_id, item_ids in tqdm(duplicates):
    for item_id in item_ids[1:]:
        try:
            es.delete(index='dblp_v12', id=item_id)
        except:
            time.sleep(60)
            es.delete(index='dblp_v12', id=item_id)
