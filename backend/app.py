from flask import Flask, request, jsonify
import psycopg2
import os
import time

app = Flask(__name__)
while True:

    try:

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        print("Connected to PostgreSQL")

        break

    except Exception as e:

        print("Database not ready")
        print(e)

        time.sleep(5)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
)
""")

conn.commit()


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


@app.route("/users", methods=["GET"])
def users():

    cur.execute("SELECT * FROM users")

    data = cur.fetchall()

    return jsonify(data)


@app.route("/users", methods=["POST"])
def add_user():

    data = request.get_json()

    cur.execute(
        "INSERT INTO users(name) VALUES(%s)",
        (data["name"],)
    )

    conn.commit()

    return {"message": "User Added"}, 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
