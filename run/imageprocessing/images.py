import os
import tempfile

from google.cloud import storage
from wand.image import Image

storage_client = storage.Client()


def blur_image(bucket_name: str, filename: str):
    if filename.startswith("blurred-"):
        print(f"the image {filename} is already blurred.")
        return

    blob = storage_client.bucket(bucket_name).get_blob(filename)

    _, temp_file = tempfile.mkstemp()
    blob.download_to_filename(temp_file)
    print(f"image {filename} was downloaded to {temp_file}")

    with Image(filename=temp_file) as image:
        image.resize(*image.size, blur=32, filter="hamming")
        image.save(filename=temp_file)

    print(f"image {filename} was blurred")

    blur_bucket_name = os.getenv("BLURRED_BUCKET_NAME")
    new_blob = storage_client.bucket(blur_bucket_name).blob(f"blurred-{filename}")
    new_blob.upload_from_filename(temp_file)
    print(f"blurred image uploaded to {blur_bucket_name}/{filename}")

    # delete temporary file
    os.remove(temp_file)
