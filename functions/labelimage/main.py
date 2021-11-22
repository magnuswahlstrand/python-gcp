import json

from google.cloud import storage, vision

storage_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()


def label_image(request):
    message = request.get_json()
    bucket_name = message["bucket"]
    file_name = message["name"]

    blob_uri = f"gs://{bucket_name}/{file_name}"
    blob_source = vision.Image(source=vision.ImageSource(gcs_image_uri=blob_uri))
    result = vision_client.safe_search_detection(image=blob_source)
    annotations = result.safe_search_annotation

    # Transform annotations to JSON
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    safe_search = {
        "adult": likelihood_name[annotations.adult],
        "medical": likelihood_name[annotations.medical],
        "spoof": likelihood_name[annotations.spoof],
        "violence": likelihood_name[annotations.violence],
        "racy": likelihood_name[annotations.racy],
    }

    # Store information in the metadata-field on the blob
    blob = storage_client.bucket(bucket_name).get_blob(file_name)

    # Create metadata dict if it doesn't exist
    metadata = blob.metadata if blob.metadata else {}
    metadata['safe_search'] = json.dumps(safe_search)
    blob.metadata = metadata
    blob.patch()

    return "OK"


# Used for local testing
if __name__ == "__main__":
    storage_event = {
        "bucket": "imageprocessing-upload",
        "name": "dog2.jpeg"
    }
    label_image(storage_event)
