import logging
import sys
from datetime import datetime

import psycopg2
from flask import Flask

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
app = Flask(__name__)

counter = 0
PERSISTENT_VOL_DIR = '/usr/persist/output'
PING_PONG_OUTPUT_FILE = 'ping-pong-output'
conn = None
cur = None


def connect_to_db():
    global conn, cur
    try:
        conn = psycopg2.connect(
            #host="0.0.0.0",
            host='db-headless-svc',
            database="postgres",
            user="postgres",
            password="foobar"
        )
        cur = conn.cursor()

        logging.info('Connected to db')
        return True
    except Exception as e:
        logging.error(f'Encountered error during database connection: {e}')
        return False


@app.route("/pingpong")
def ping_pong():
    global counter

    counter += 1
    return f'pongUpdated: {counter}'


@app.route("/pingpong-file")
def ping_pong_file():
    global counter

    counter += 1
    open(f'{PERSISTENT_VOL_DIR}/{PING_PONG_OUTPUT_FILE}', 'w').write(f'count: {counter}')
    return f'pong: {counter}'


@app.route("/pingpong-db")
def ping_pong_db():
    cur.execute('select * from ping_pong order by id desc limit 1')
    query_result = cur.fetchone()

    cur_ping = -1
    if query_result:
        cur_ping = query_result[0]

    cur.execute('insert into ping_pong (num_ping) values (%s)', (cur_ping + 1,))
    conn.commit()

    return f'pong: {cur_ping}'


@app.route("/is-ready")
def is_ready():
    logging.info(f'Readiness probe at {datetime.now()}')

    #if (not conn or not cur) and not connect_to_db():
    #    return 'error', 500

    return 'ok', 200


if __name__ == '__main__':
    #connect_to_db()
    app.run(host="0.0.0.0", port=3001)
