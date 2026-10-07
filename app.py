import hashlib
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    user_id = request.args.get("id", "1")
    # Дефект №1: отражённая XSS (Bandit не найдёт — нет taint-анализа)
    return f"<h1>Hello, user #{user_id}!</h1>"


@app.route("/checksum")
def checksum():
    data = request.args.get("data", "")
    # Дефект №2: слабый хэш MD5 (B324)
    return hashlib.md5(data.encode()).hexdigest()


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # Дефект №3: инъекция команд ОС (B602)
    result = subprocess.run(
        f"ping -c 1 {host}", shell=True, capture_output=True, check=False
    )
    return f"<pre>{result.stdout.decode()}</pre>"


if __name__ == "__main__":
    # Дефект №4: debug=True даёт RCE (B201)
    app.run(debug=True)

