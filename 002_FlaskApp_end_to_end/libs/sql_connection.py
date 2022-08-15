
# required library imports
import pandas as pd
import psycopg2

import yaml
import warnings

warnings.filterwarnings('ignore')

# read connection.yaml
with open('connection.yaml', 'r') as file:
    infos = yaml.safe_load(file)

# connect database
conn = psycopg2.connect(user= infos['user'],
                        password= infos['password'],
                        host= infos['host'],
                        database= infos['database'])

def read_songtable(query):
    df = pd.read_sql(query, conn)
    return df

insert_query = """
        INSERT INTO songtable (singer, song, album, lyrics)
        VALUES (%s, %s, %s, %s)
        """

def insert_songtable(values):
    conn = psycopg2.connect(user= infos['user'],
                            password= infos['password'],
                            host= infos['host'],
                            database= infos['database'])

    cursor = conn.cursor()

    cursor.execute(insert_query, tuple(values))

    conn.commit()

    cursor.close()
    print('values inserted succesfully')