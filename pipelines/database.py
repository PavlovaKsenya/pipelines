import psycopg2
from psycopg2 import Error
from .utils import print_error
import sys


class PostrgesDB:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user='postgres',
                                  password='1234',
                                  host="db",
                                  port="5432",
                                  database='pipelines')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print_error(f"Ошибка PostgreSQL: {error}")
            sys.exit(1)

    def run_query(self, query):
        try:
            self.cursor.execute(query)
        except (Exception, Error) as error:
            print_error(f"Ошибка PostgreSQL: {error}")
            sys.exit(1)

    def load_data_to_table(self, input_file, table):
        sql = f"COPY {table} FROM STDIN DELIMITER ',' CSV HEADER"
        self.cursor.copy_expert(sql, open(input_file, "r"))

    def copy_data_to_file(self, table, output_file):
        sql = f"COPY (SELECT * FROM {table}) TO STDOUT DELIMITER ',' CSV HEADER"
        self.cursor.copy_expert(sql, open(output_file, "w"))

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

