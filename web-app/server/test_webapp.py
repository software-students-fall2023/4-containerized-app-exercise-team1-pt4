"""
Module for testing the web application.
"""

from unittest.mock import MagicMock
from io import BytesIO
import os
import pytest
from werkzeug.datastructures import FileStorage


# Mock environment variables
os.environ["MONGO_INITDB_ROOT_USERNAME"] = "testuser"
os.environ["MONGO_INITDB_ROOT_PASSWORD"] = "testpassword"

from app import app as flask_app


@pytest.fixture
def flask_app_fixture():
    """Provides a testing app fixture."""
    flask_app.config["TESTING"] = True
    flask_app.config["UPLOADS"] = "./uploads"
    flask_app.secret_key = "testsecret"
    flask_app.config["MONGO_URI"] = "mongodb://localhost:27017/test_db"
    return flask_app


@pytest.fixture
def client(flask_app_fixture):
    """Provides a testing client fixture."""
    with flask_app_fixture.test_client() as testing_client:
        yield testing_client


@pytest.fixture
def mock_requests_post(monkeypatch):
    """Provides a mock for requests.post."""
    mock_post = MagicMock()
    monkeypatch.setattr("requests.post", mock_post)
    return mock_post


# Mock MongoDB interactions
@pytest.fixture(autouse=True)
def mock_mongo(monkeypatch):
    """Mocks MongoDB interactions."""
    mock_mongo_client = MagicMock()
    monkeypatch.setattr("pymongo.MongoClient", mock_mongo_client)
    return mock_mongo_client


def test_upload_without_file(client):
    """Test uploading without a file."""
    response = client.post("/transcribe", data={})
    assert response.status_code == 302


def test_upload_with_empty_file_name(client):
    """Test uploading with an empty file name."""
    data = {"file": (BytesIO(), "")}
    response = client.post("/transcribe", data=data)
    assert response.status_code == 302


def test_transcription_success(client, mock_requests_post, monkeypatch):
    """Test successful transcription."""
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {
        "transcript": "test transcription"
    }

    def mock_save(*args, **kwargs):
        pass  # Mock the save method to do nothing

    monkeypatch.setattr(FileStorage, "save", mock_save)

    data = {
        "file": (
            FileStorage(stream=BytesIO(b"fake audio data"), filename="test_audio.mp3"),
            "test_audio.mp3",
        )
    }
    response = client.post("/transcribe", data=data)
    assert response.status_code == 200
    assert response.json == {"transcript": "test transcription"}


def test_transcription_api_failure(client, mock_requests_post, monkeypatch):
    """Test transcription API failure."""
    mock_requests_post.return_value.status_code = 500
    mock_requests_post.return_value.json.return_value = {"error": "API failure"}

    def mock_save(*args, **kwargs):
        pass  # Mock the save method to do nothing

    monkeypatch.setattr(FileStorage, "save", mock_save)

    data = {
        "file": (
            FileStorage(stream=BytesIO(b"fake audio data"), filename="test_audio.mp3"),
            "test_audio.mp3",
        )
    }
    response = client.post("/transcribe", data=data)
    assert response.status_code == 500
    assert "error" in response.json


def test_upload_with_actual_file_part_no_filename(client):
    """Test uploading with an actual file part but no filename."""
    data = {"file": (BytesIO(b"audio data"), "")}
    response = client.post("/transcribe", data=data)
    assert response.status_code == 302
