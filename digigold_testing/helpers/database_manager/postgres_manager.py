import psycopg2
from psycopg2 import sql
import digigold_testing.config as config


class PostgresSQLManager:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=config.PSQL_DATABASE,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            host=config.PSQL_HOST,
            port=config.PSQL_PORT
        )
        self.cursor = self.connection.cursor()

    def query_data(self, table_name, condition=None):
        query = sql.SQL(f"SELECT * FROM {table_name}")
        if condition:
            query += sql.SQL(" WHERE {}").format(condition)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_total_gold(self):
        query = sql.SQL(f'SELECT quantity_after_transaction FROM stock_ledgers order by created_at desc limit 1')
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_unallocated_gold(self):
        query = sql.SQL(f'SELECT * FROM racks')
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
