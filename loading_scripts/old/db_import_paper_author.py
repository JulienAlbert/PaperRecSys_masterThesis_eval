import json
import psycopg2
from tqdm import tqdm

paper_author_path = 'paper_author.json'

connection = psycopg2.connect(host="localhost",port=5432, database="dblp_v12", 
                              user="dblp_v12", password="dblp_v12")

cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS paper_author""")

cursor.execute("""CREATE TABLE paper_author(
                paper_id BIGINT NOT NULL,
                author_id BIGINT NOT NULL,
                PRIMARY KEY (paper_id, author_id));""")

connection.commit()

with open(paper_author_path) as file:
    for paper_id, author_id in tqdm(json.load(file)):
        cursor.execute("""INSERT INTO paper_author (paper_id, author_id)
                          VALUES (%(paper_id)s, %(author_id)s)""",
                       {'paper_id': paper_id,
                        'author_id': author_id})

connection.commit()

cursor.execute("""ALTER TABLE paper_author
                  ADD FOREIGN KEY (paper_id) REFERENCES paper(id)""")

cursor.execute("""ALTER TABLE paper_author
                  ADD FOREIGN KEY (author_id) REFERENCES author(id)""")

connection.commit()

cursor.execute("SELECT COUNT(*) FROM paper_author")
print(cursor.fetchone())

cursor.close()
connection.close()