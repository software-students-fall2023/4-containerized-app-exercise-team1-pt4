"""
This module contains tests for the ML Client app.
"""

import io
from unittest.mock import patch, AsyncMock
import pytest

# Mock the Deepgram and MongoDB setup before importing the app
with patch("deepgram.Deepgram"):
    with patch("pymongo.MongoClient"):
        from app import app

@pytest.fixture
def client():
    """Yields a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client

def test_successful_transcription(client):
    """Tests successful audio transcription."""
    mock_deepgram_response = AsyncMock(
        return_value={
            "results": {
                "channels": [{"alternatives": [{"transcript": "Test transcript"}]}]
            }
        }
    )

    with patch("app.deepgram.transcription.prerecorded", new=mock_deepgram_response):
        with patch("pymongo.collection.Collection.insert_one") as mock_insert:
            data = {"file": (io.BytesIO(b"audio data"), "audio.mp3")}
            response = client.post("/api", data=data, content_type="multipart/form-data")
            assert mock_insert.called
            assert response.status_code == 200
            assert "transcription" in response.json
            assert response.json["transcription"] == "Test transcript"

def test_transcription_with_no_file(client):
    """Tests handling of transcription request with no file provided."""
    with pytest.raises(ValueError, match="No file provided for transcription."):
        client.post("/api", data={}, content_type="multipart/form-data")

def test_deepgram_valid_response_no_transcript(client):
    """Tests handling of valid Deepgram response with no transcript."""
    mock_deepgram_response = AsyncMock(
        return_value={"results": {"channels": [{"alternatives": [{"transcript": ""}]}]}}
    )

    with patch("app.deepgram.transcription.prerecorded", new=mock_deepgram_response):
        with patch("pymongo.collection.Collection.insert_one") as mock_insert:
            data = {"file": (io.BytesIO(b"audio data"), "audio.mp3")}
            response = client.post("/api", data=data, content_type="multipart/form-data")
            assert mock_insert.called
            assert response.status_code == 200
            assert "transcription" in response.json
            assert response.json["transcription"] == ""

def test_transcription_with_invalid_file_type(client):
    """Tests transcription handling with an invalid file type."""
    mock_deepgram_response = AsyncMock(
        return_value={"results": {"channels": [{"alternatives":
                                                [{"transcript": "Valid transcription"}]}]}}
    )

    with patch('app.deepgram.transcription.prerecorded', new=mock_deepgram_response):
        with patch('pymongo.collection.Collection.insert_one') as mock_insert:
            data = {"file": (io.BytesIO(b"Not an audio file"), "invalid_file.txt")}
            response = client.post("/api", data=data, content_type="multipart/form-data")
            assert mock_insert.called
            assert response.status_code == 200
            assert "transcription" in response.json
            assert response.json["transcription"] == "Valid transcription"

def test_transcription_with_empty_audio_file(client):
    """Tests transcription handling with an empty audio file."""
    mock_deepgram_response = AsyncMock(
        return_value={"results": {"channels": [{"alternatives": [{"transcript": ""}]}]}}
    )

    with patch("pymongo.collection.Collection.insert_one"):
        with patch("app.deepgram.transcription.prerecorded", new=mock_deepgram_response):
            data = {"file": (io.BytesIO(b""), "audio.mp3")}
            response = client.post("/api", data=data, content_type="multipart/form-data")
            assert response.status_code == 200
            assert "transcription" in response.json
            assert response.json["transcription"] == ""
