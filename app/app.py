import os

from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "status": "UP",
            "database": "UP"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "DOWN",
            "database": "DOWN",
            "error": str(e)
        }), 503


@app.route("/environment")
def environment():
    return jsonify({
        "environment": os.getenv("APP_ENV", "UNKNOWN")
    })


@app.route("/version")
def version():
    return jsonify({
        "version": os.getenv("APP_VERSION", "UNKNOWN")
    })


@app.route("/customers")
def customers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(200) NOT NULL
            )
        """)

        cursor.execute("""
            SELECT id, name, email
            FROM customers
            ORDER BY id
        """)

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
        return jsonify({"error": str(e)}), 500


@app.route("/customers/search")
def search_customers():
    name = request.args.get("name", "")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(200) NOT NULL
            )
        """)

        cursor.execute("""
            SELECT id, name, email
            FROM customers
            WHERE name ILIKE %s
            ORDER BY id
        """, (f"%{name}%",))

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
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
