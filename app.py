import hashlib
import ipaddress
import subprocess

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    user_id = request.args.get("id", "1")
    # Исправление №1: экранирование
    return f"<h1>Hello, user #{escape(user_id)}!</h1>"


@app.route("/checksum")
def checksum():
    data = request.args.get("data", "")
    # Исправление №2: стойкий хэш
    return hashlib.sha256(data.encode()).hexdigest()


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # Исправление №3, слой 1: валидация allow-list
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return "Invalid IP address", 400

    # Исправление №3, слой 2: shell=False
    result = subprocess.run(
        ["/bin/ping", "-c", "1", host],
        capture_output=True,
        check=False,
        timeout=5,
    )
    return f"<pre>{escape(result.stdout.decode())}</pre>"


if __name__ == "__main__":
    # Исправление №4: debug выключен
    app.run(debug=False)
