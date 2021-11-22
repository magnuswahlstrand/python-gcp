import mock
import pytest

import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_payload_empty(client):
    r = client.post("/", json="")
    assert r.status_code == 400


def test_payload_json_empty(client):
    r = client.post("/", json={})
    assert r.status_code == 400


@mock.patch("images.blur_image", mock.MagicMock(side_effect=Exception('some test exception')))
def test_blur_images_raises_exception(client):
    r = client.post("/", json={"name": "foo", "bucket": "bar"})
    assert r.status_code == 500


@mock.patch("images.blur_image", mock.MagicMock())
def test_valid_message(client):
    r = client.post("/", json={"name": "foo", "bucket": "bar"})
    assert r.status_code == 201


@mock.patch("images.blur_image", mock.MagicMock())
def test_valid_real_message(client):
    # Event from trigger of type "google.cloud.storage.object.v1.finalized"
    # Captured 2021-11-18
    real_event = {
        'kind': 'storage#object',
        'id': 'imageprocessing-upload/dogs.png/1637268472503552',
        'selfLink': 'https://www.googleapis.com/storage/v1/b/imageprocessing-upload/o/dogs.png',
        'name': 'dogs.png',
        'bucket': 'imageprocessing-upload',
        'generation': '1637268472503552',
        'metageneration': '1',
        'contentType': 'image/png',
        'timeCreated': '2021-11-18T20:47:52.578Z',
        'updated': '2021-11-18T20:47:52.578Z',
        'storageClass': 'STANDARD',
        'timeStorageClassUpdated': '2021-11-18T20:47:52.578Z',
        'size': '93164',
        'md5Hash': '9EjYqkENGpV8Grzwqqpqmg==',
        'mediaLink': 'https://www.googleapis.com/download/storage/v1/b/imageprocessing-upload/o/dogs.png?generation=1637268472503552&alt=media',
        'contentLanguage': 'en',
        'crc32c': '/Ytgmw==',
        'etag': 'CIC60q3kovQCEAE='
    }
    r = client.post("/", json=real_event)
    assert r.status_code == 201
