import os

from flask import Flask, render_template
from google.cloud import storage

app = Flask(__name__)

storage_client = storage.Client()


@app.route("/", methods=["POST"])
def generate_static_site():
    print('received request!')
    source_bucket_name = os.getenv("SOURCE_BUCKET_NAME")
    target_bucket_name = os.getenv("TARGET_BUCKET_NAME")

    html = render_site_html(source_bucket_name)
    index_blob = storage_client.bucket(target_bucket_name).blob("index3.html")
    index_blob.upload_from_string(html, content_type='text/html')
    print(f"uploaded static file to {target_bucket_name}/index3.html")
    return html


# Used for local development
@app.route("/", methods=["GET"])
def show_static_site():
    print('received request!')
    source_bucket_name = os.getenv("SOURCE_BUCKET_NAME")
    return render_site_html(source_bucket_name)


def render_site_html(source_bucket_name):
    images = list(storage_client.list_blobs(source_bucket_name))
    print(f"rendering html site, found {len(images)} images")
    return render_template("index.html", images=images)
