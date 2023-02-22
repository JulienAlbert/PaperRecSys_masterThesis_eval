import json
import psycopg2
from tqdm import tqdm

author_paths = ['author_c1.json', 'author_c2.json']

connection = psycopg2.connect(host="localhost",port=5432, database="dblp_v12", 
                              user="dblp_v12", password="dblp_v12")

cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS author""")

cursor.execute("""CREATE TABLE author(
                id BIGINT PRIMARY KEY,
                name TEXT NOT NULL,
                org TEXT,
                paper_ids TEXT);""")

connection.commit()

for author_path in author_paths:
    with open(author_path) as file:
        for author in tqdm(json.load(file)):
            if 'org' not in author or not author['org']:
                author['org'] = None
            if 'paper_ids' not in author or not author['paper_ids']:
                author['paper_ids'] = None
            
            try:
                cursor.execute("""INSERT INTO author (id, name, org, paper_ids)
                            VALUES (%(id)s, %(name)s, %(org)s, %(paper_ids)s)""",
                        {'id': author['id'],
                            'name': author['name'],
                            'org': author['org'],
                            'paper_ids': json.dumps(author['paper_ids'])})
            except:
                print(author)
                cursor.execute("""INSERT INTO author (id, name, org, paper_ids)
                    VALUES (2939411041, 'Zhe-Yu Wang', 'National Central University, Taiwan', '[2938438733]')""")

    connection.commit()

cursor.execute("SELECT COUNT(*) FROM author")
print(cursor.fetchone())

cursor.close()
connection.close()