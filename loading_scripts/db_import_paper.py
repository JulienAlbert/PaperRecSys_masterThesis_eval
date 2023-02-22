import os
import json
import psycopg2
from tqdm import tqdm

paper_paths = [f for f in os.listdir('./') if 'chunk' in f]

connection = psycopg2.connect(host="localhost",port=5432, database="dblp_v12", 
                              user="dblp_v12", password="dblp_v12")

cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS paper_author""")
cursor.execute("""DROP TABLE IF EXISTS paper_fos""")
cursor.execute("""DROP TABLE IF EXISTS paper_ref_paper""")

cursor.execute("""DROP TABLE IF EXISTS paper""")

cursor.execute("""CREATE TABLE paper(
                id BIGINT PRIMARY KEY,
                title TEXT NOT NULL,
                venue_id BIGINT,
                year INTEGER,
                n_citation INTEGER,
                page_start TEXT,
                page_end TEXT,
                doc_type TEXT,
                publisher TEXT,
                volume TEXT,
                issue TEXT,
                doi TEXT,
                abstract TEXT,
                reference_ids TEXT,
                citation_ids TEXT,
                author_ids TEXT,
                fos_ids TEXT);""")

connection.commit()

for path in tqdm(paper_paths):
    with open(path) as file:
        for paper in tqdm(json.load(file)):
            if 'venue_id' not in paper:
                paper['venue_id'] = None
            if 'year' not in paper:
                paper['year'] = None
            if 'n_citation' not in paper:
                paper['n_citation'] = None
            if 'page_start' not in paper:
                paper['page_start'] = None
            if 'page_end' not in paper:
                paper['page_end'] = None
            if 'doc_type' not in paper:
                paper['doc_type'] = None
            if 'publisher' not in paper:
                paper['publisher'] = None
            if 'volume' not in paper:
                paper['volume'] = None
            if 'issue' not in paper:
                paper['issue'] = None
            if 'doi' not in paper:
                paper['doi'] = None
            if 'abstract' not in paper:
                paper['abstract'] = None
            if 'reference_ids' not in paper:
                paper['reference_ids'] = None
            if 'citation_ids' not in paper:
                paper['citation_ids'] = None
            if 'author_ids' not in paper:
                paper['author_ids'] = None
            if 'fos_ids' not in paper:
                paper['fos_ids'] = None
            

            cursor.execute("""INSERT INTO paper (id, title, venue_id, year, n_citation, page_start, 
                              page_end, doc_type, publisher, volume, issue, doi, abstract,
                              reference_ids, citation_ids, author_ids, fos_ids) VALUES 
                              (%(id)s, %(title)s, %(venue_id)s, %(year)s, %(n_citation)s, %(page_start)s,
                               %(page_end)s, %(doc_type)s, %(publisher)s, %(volume)s, %(issue)s, %(doi)s,
                               %(abstract)s, %(reference_ids)s, %(citation_ids)s, %(author_ids)s, %(fos_ids)s)""",
                           {'id': paper['id'],
                            'title': paper['title'],
                            'venue_id': paper['venue_id'],
                            'year': paper['year'],
                            'n_citation': paper['n_citation'],
                            'page_start': paper['page_start'],
                            'page_end': paper['page_end'],
                            'doc_type': paper['doc_type'],
                            'publisher': paper['publisher'],
                            'volume': paper['volume'],
                            'issue': paper['issue'],
                            'doi': paper['doi'],
                            'abstract': paper['abstract'],
                            'reference_ids': json.dumps(paper['reference_ids']),
                            'citation_ids': json.dumps(paper['citation_ids']),
                            'author_ids': json.dumps(paper['author_ids']),
                            'fos_ids': json.dumps(paper['fos_ids'])})
        
        connection.commit()

cursor.execute("SELECT COUNT(*) FROM paper")
print(cursor.fetchone())

cursor.close()
connection.close()