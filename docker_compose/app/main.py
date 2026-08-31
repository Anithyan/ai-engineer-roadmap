import os
import time

import psycopg


def main():

    host = os.environ["DB_HOST"]
    print(f"Connexion a Postgres (host={host})...", flush=True)

    conn = psycopg.connect(
        host=host,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    print("OK Connecte a Postgres !", flush=True)

    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS heartbeats ("
            "id SERIAL PRIMARY KEY, "
            "created_at TIMESTAMPTZ DEFAULT now())"
        )
    conn.commit()

    while True:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO heartbeats DEFAULT VALUES")
            cur.execute("SELECT count(*) FROM heartbeats")
            total = cur.fetchone()[0]
        conn.commit()
        print(f"heartbeat insere - total en base : {total}", flush=True)
        time.sleep(5)


if __name__ == "__main__":
    main()
