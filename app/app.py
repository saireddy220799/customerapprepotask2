import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

ENVIRONMENT = os.getenv("ENVIRONMENT", "UNKNOWN")
VERSION = os.getenv("APP_VERSION", "UNKNOWN")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "customerdb")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5
    )


@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "status": "UP",
            "environment": ENVIRONMENT,
            "version": VERSION,
            "database": "reachable"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "DOWN",
            "environment": ENVIRONMENT,
            "version": VERSION,
            "database": "unreachable",
            "error": str(e)
        }), 500


@app.route("/customers")
def customers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL
            )
        """)

        conn.commit()

        cursor.execute(
            "SELECT id, name, email FROM customers ORDER BY id"
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify([
            {
                "id": row[0],
                "name": row[1],
                "email": row[2]
            }
            for row in rows
        ])

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/info")
def info():
    return jsonify({
        "application": "customer-app",
        "environment": ENVIRONMENT,
        "version": VERSION
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )
