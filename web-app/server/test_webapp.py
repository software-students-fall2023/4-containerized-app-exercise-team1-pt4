"""
Module for testing the web application.
"""
from unittest.mock import MagicMock
from io import BytesIO
import pytest
from werkzeug.datastructures import FileStorage

# Import app from the correct location. Adjust as necessary based on your project structure
from app import app as flask_app

@pytest.fixture
def flask_app_fixture():
    """Provides a testing app fixture."""
    flask_app.config['TESTING'] = True
    flask_app.config['UPLOADS'] = './uploads'
    flask_app.secret_key = 'testsecret'
    flask_app.config['MONGO_URI'] = "mongodb://localhost:27017/test_db"  # Adjust as necessary
    return flask_app

@pytest.fixture
def client_fixture(flask_app_fixture):
    """Provides a testing client fixture."""
    with flask_app_fixture.test_client() as testing_client:
        yield testing_client

@pytest.fixture
def mock_requests_post_fixture(monkeypatch):
    """Provides a mock for requests.post."""
    mock_post = MagicMock()
    monkeypatch.setattr("requests.post", mock_post)
    return mock_post

def test_upload_without_file(client_fixture):
    """Test uploading without a file."""
    response = client_fixture.post("/transcribe", data={})
    assert response.status_code == 302

def test_upload_with_empty_file_name(client_fixture):
    """Test uploading with an empty file name."""
    data = {"file": (BytesIO(), "")}
    response = client_fixture.post("/transcribe", data=data)
    assert response.status_code == 302

def test_transcription_success(client_fixture, mock_requests_post_fixture, monkeypatch):
    """Test successful transcription."""
    mock_requests_post_fixture.return_value.status_code = 200
    mock_requests_post_fixture.return_value.json.return_value = {"transcript": "test transcription"}

    def mock_save(_, __):
        pass  # Mock the save method to do nothing

    monkeypatch.setattr(FileStorage, "save", mock_save)

    data = {'file': (FileStorage(stream=BytesIO(b"fake audio data"),
                                 filename='test_audio.mp3'), 'test_audio.mp3')}
    response = client_fixture.post("/transcribe", data=data)
    assert response.status_code == 200
    assert response.json == {"transcript": "test transcription"}

def test_transcription_api_failure(client_fixture, mock_requests_post_fixture, monkeypatch):
    """Test transcription API failure."""
    mock_requests_post_fixture.return_value.status_code = 500
    mock_requests_post_fixture.return_value.json.return_value = {"error": "API failure"}

    def mock_save(_, __):
        pass  # Mock the save method to do nothing

    monkeypatch.setattr(FileStorage, "save", mock_save)

    data = {'file': (FileStorage(stream=BytesIO(b"fake audio data"),
                                 filename='test_audio.mp3'), 'test_audio.mp3')}
    response = client_fixture.post("/transcribe", data=data)
    assert response.status_code == 500
    assert "error" in response.json

def test_upload_with_actual_file_part_no_filename(client_fixture):
    """Test uploading with an actual file part but no filename."""
    data = {"file": (BytesIO(b"audio data"), "")}
    response = client_fixture.post("/transcribe", data=data)
    assert response.status_code == 302
