"""
DB bootstrap Lambda.

Creates the per-service databases on the shared Postgres instance.
Idempotent: re-running is a no-op once databases exist.

Invoked once per `terraform apply` via aws_lambda_invocation. Pure Python
(pg8000) so no native deps are required when packaging.
"""

import json
import os

import pg8000.native


def handler(event, context):
    host = os.environ["DB_HOST"]
    port = int(os.environ.get("DB_PORT", "5432"))
    master_user = os.environ["DB_USER"]
    master_db = os.environ["DB_NAME"]
    password = os.environ["DB_PASSWORD"]
    databases = json.loads(os.environ["DATABASES"])  # list of db names

    conn = pg8000.native.Connection(
        user=master_user,
        password=password,
        host=host,
        port=port,
        database=master_db,
    )

    created = []
    skipped = []
    try:
        existing = {
            row[0]
            for row in conn.run("SELECT datname FROM pg_database")
        }
        for db in databases:
            if db in existing:
                skipped.append(db)
                continue
            # CREATE DATABASE cannot be parameterized; the name is validated below.
            if not db.replace("_", "").isalnum():
                raise ValueError(f"Refusing to create database with name: {db!r}")
            conn.run(f'CREATE DATABASE "{db}"')
            created.append(db)
    finally:
        conn.close()

    return {"created": created, "skipped": skipped}
