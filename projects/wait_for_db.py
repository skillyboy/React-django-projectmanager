import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='skilly1234',
                host='db',
                port='5432'
            )
            conn.close()
            break
        except OperationalError:
            time.sleep(1)

if __name__ == '__main__':
    wait_for_db()
