import json
import psycopg2
from tqdm import tqdm

venue_path = 'venue.json'

connection = psycopg2.connect(host="localhost",port=5432, database="dblp_v12", 
                              user="dblp_v12", password="dblp_v12")

cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS venue""")

cursor.execute("""CREATE TABLE venue(
                id BIGINT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT,
                paper_ids TEXT);""")

connection.commit()

with open(venue_path) as file:
    for venue in tqdm(json.load(file).values()):
        if 'type' not in venue or not venue['type']:
            venue['type'] = None
        if 'paper_ids' not in venue or not venue['paper_ids']:
            venue['paper_ids'] = None
        
        cursor.execute("""INSERT INTO venue (id, name, type, paper_ids)
                          VALUES (%(id)s, %(name)s, %(type)s, %(paper_ids)s)""",
                       {'id': venue['id'],
                        'name': venue['raw'],
                        'type': venue['type'],
                        'paper_ids': json.dumps(venue['paper_ids'])})

connection.commit()

cursor.execute("SELECT COUNT(*) FROM venue")
print(cursor.fetchone())

cursor.close()
connection.close()