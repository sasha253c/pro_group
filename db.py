import psycopg2
from psycopg2 import sql

from config import config_db


class DB_Helper:
    def __init__(self):
        self.driver = psycopg2.connect(database=config_db['database'],
                                       user=config_db['user'],
                                       password=config_db['password'],
                                       host=config_db['host'])
        self.driver.autocommit = True
        self.create_table()

    def create_table(self):
        """
        Create table 'best_pairs' if not exists
        """
        with self.driver.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS best_pairs (id SERIAL PRIMARY KEY,
                                                                     datetime TIMESTAMP NOT NULL);''')

    def add(self, best_pair):
        """
        Add new row to table 'best_pairs'
        """
        with self.driver.cursor() as cursor:
            # add new columns 'PAIR_ASK', 'PAIR_BID' to the table
            cursor.execute('''SELECT column_name FROM information_schema.columns WHERE
                              table_name = 'best_pairs';''')
            columns = [x[0] for x in cursor.fetchall()]
            for key in best_pair.keys():
                if key not in columns:
                    query = sql.SQL("ALTER TABLE best_pairs ADD COLUMN {} DOUBLE PRECISION;")
                    cursor.execute(query.format(sql.Identifier(key)))

            # dictionary 'best_pair' insert to the table
            keys = best_pair.keys()
            columns = '"' + '","'.join([k for k in keys]) + '"'
            values = ','.join(['%({})s'.format(k) for k in keys])
            insert = 'INSERT INTO best_pairs ({0}) VALUES ({1});'.format(columns, values)
            cursor.execute(cursor.mogrify(insert, best_pair))

    def destroy(self):
        self.driver.close()