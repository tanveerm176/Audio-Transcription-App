import pytest
from transcription_service import transcribe_audio

def test_transcribe_audio_with_valid_file():
    # Add your test logic here
    result = transcribe_audio("test_audio.wav")
    assert result is not None
    assert "text" in result

def test_transcribe_audio_with_invalid_file():
    with pytest.raises(FileNotFoundError):
        transcribe_audio("nonexistent.wav")