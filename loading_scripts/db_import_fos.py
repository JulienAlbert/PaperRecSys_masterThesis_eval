import json
import psycopg2
from tqdm import tqdm

fos_path = 'fos.json'

connection = psycopg2.connect(host="localhost",port=5432, database="dblp_v12", 
                              user="dblp_v12", password="dblp_v12")

cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS fos""")

cursor.execute("""CREATE TABLE fos(
                id BIGINT PRIMARY KEY,
                name TEXT NOT NULL,
                paper_ids TEXT);""")

connection.commit()

with open(fos_path) as file:
    for fos in tqdm(json.load(file).values()):
        if 'paper_ids' not in fos or not fos['paper_ids']:
            fos['paper_ids'] = None
        
        cursor.execute("""INSERT INTO fos (id, name, paper_ids)
                          VALUES (%(id)s, %(name)s, %(paper_ids)s)""",
                       {'id': fos['id'],
                        'name': fos['name'],
                        'paper_ids': json.dumps(fos['paper_ids'])})

connection.commit()

cursor.execute("SELECT COUNT(*) FROM fos")
print(cursor.fetchone())

cursor.close()
connection.close()