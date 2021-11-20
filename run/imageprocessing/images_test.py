import uuid

import mock
from mock import MagicMock

import images


@mock.patch("images.os")
@mock.patch("images.Image")
@mock.patch("images.storage_client")
def test_blur_image(storage_client, image_mock, os_mock, capsys):
    filename = str(uuid.uuid4())
    blur_bucket = "blurred-bucket-" + str(uuid.uuid4())

    os_mock.remove = MagicMock()
    os_mock.path = MagicMock()

    os_mock.getenv = MagicMock(return_value=blur_bucket)

    image_mock.return_value = image_mock
    image_mock.__enter__.return_value = image_mock

    bucket = "somebucket"
    filename = str(uuid.uuid4())

    images.blur_image(bucket, filename)

    out, _ = capsys.readouterr()

    assert f"image {filename} was downloaded to" in out
    assert f"image {filename} was blurred" in out
    assert f"blurred image uploaded to {blur_bucket}/{filename}" in out

    assert image_mock.resize.called
    assert image_mock.save.called
    assert os_mock.remove.called
