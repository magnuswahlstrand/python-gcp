from flask import Flask, request

import images

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    print('received request!')
    message = request.get_json()

    if not message or "bucket" not in message or "name" not in message:
        msg = "invalid cloud storage message"
        print(f"error: {msg}")
        return f"bad request: {msg}", 400

    try:
        images.blur_image(message["bucket"], message["name"])
        return "", 201
    except Exception as e:
        print(f'error: {e}')
        return "", 500
