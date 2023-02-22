import json
import psycopg2
from tqdm import tqdm

paper_fos_paths = ['paper_fos_c1.json', 'paper_fos_c2.json']

connection = psycopg2.connect(host="localhost",port=5432, database="dblp_v12", 
                              user="dblp_v12", password="dblp_v12")

cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS paper_fos""")

cursor.execute("""CREATE TABLE paper_fos(
                paper_id BIGINT NOT NULL,
                fos_id BIGINT NOT NULL,
                PRIMARY KEY (paper_id, fos_id));""")

connection.commit()

for paper_fos_path in paper_fos_paths:
    with open(paper_fos_path) as file:
        count = 0
        for paper_id, fos_id in tqdm(json.load(file)):
            cursor.execute("""INSERT INTO paper_fos (paper_id, fos_id)
                            VALUES (%(paper_id)s, %(fos_id)s)""",
                        {'paper_id': paper_id,
                            'fos_id': fos_id})
            
            count += 1
            if count > 1000:
                connection.commit()
                count = 0

    connection.commit()

cursor.execute("""ALTER TABLE paper_fos
                  ADD FOREIGN KEY (paper_id) REFERENCES paper(id)""")

cursor.execute("""ALTER TABLE paper_fos
                  ADD FOREIGN KEY (fos_id) REFERENCES fos(id)""")

connection.commit()

cursor.execute("SELECT COUNT(*) FROM paper_fos")
print(cursor.fetchone())

cursor.close()
connection.close()