import json
import psycopg2
from tqdm import tqdm

paper_paper_paths = ['paper_paper_c1.json', 'paper_paper_c2.json']

connection = psycopg2.connect(host="localhost",port=5432, database="dblp_v12", 
                              user="dblp_v12", password="dblp_v12")

cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS paper_ref_paper""")

cursor.execute("""CREATE TABLE paper_ref_paper(
                paper_id BIGINT NOT NULL,
                ref_paper_id BIGINT NOT NULL,
                PRIMARY KEY (paper_id, ref_paper_id));""")

connection.commit()

for paper_paper_path in paper_paper_paths:
    with open(paper_paper_path) as file:
        count = 0
        for paper_id, ref_paper_id in tqdm(json.load(file)):
            cursor.execute("""INSERT INTO paper_ref_paper (paper_id, ref_paper_id)
                            VALUES (%(paper_id)s, %(ref_paper_id)s)""",
                        {'paper_id': paper_id,
                            'ref_paper_id': ref_paper_id})
            
            count += 1
            if count > 1000:
                connection.commit()
                count = 0

    connection.commit()

cursor.execute("""ALTER TABLE paper_ref_paper
                  ADD FOREIGN KEY (paper_id) REFERENCES paper(id)""")

cursor.execute("""ALTER TABLE paper_ref_paper
                  ADD FOREIGN KEY (ref_paper_id) REFERENCES paper(id)""")

connection.commit()

cursor.execute("SELECT COUNT(*) FROM paper_ref_paper")
print(cursor.fetchone())

cursor.close()
connection.close()