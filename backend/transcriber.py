"""
Audio transcription module using OpenAI's Whisper model.

This module provides transcription services for converting audio files to text.
It uses a singleton pattern to maintain a single instance of the Whisper model
throughout the application lifecycle, improving performance and memory usage.
"""

import whisper
import logging
from pathlib import Path
from config import settings

# Configure logger for this module
logger = logging.getLogger(__name__)


class TranscriptionService:
    """
    Service class for transcribing audio files using OpenAI's Whisper model.
    
    This class encapsulates the Whisper transcription model and provides methods
    to transcribe audio files. The model is loaded once during initialization
    to optimize performance.
    """
    
    def __init__(self):
        """
        Initialize the TranscriptionService by loading the Whisper model.
        
        Loads the Whisper model specified in application settings and logs
        the loading status. The model is loaded once and reused for all
        transcription operations.
        """
        logger.info(f"Loading Whisper model: {settings.whisper_model}")
        
        self.model = whisper.load_model(settings.whisper_model)
        
        logger.info("Whisper model loaded successfully")
        
        
    def transcribe_audio(self, file_path: str) -> dict:
        """
        Transcribe an audio file to text using the Whisper model.
        
        Converts the audio file at the specified path to text using the loaded
        Whisper model. Includes error handling to gracefully handle transcription
        failures and logs all operations for debugging.
        
        Args:
            file_path (str): The path to the audio file to transcribe.
        
        Returns:
            dict: A dictionary containing:
                - success (bool): True if transcription succeeded, False otherwise.
                - text (str): The transcribed text (None if transcription failed).
                - language (str): The detected language of the audio.
                - duration (float): The duration of the audio file in seconds.
                - error (str): Error message if transcription failed (None on success).
        
        Example:
            result = service.transcribe_audio('audio.mp3')
            if result['success']:
                print(result['text'])
            else:
                print(f"Error: {result['error']}")
        """
        
        try:
            logger.info(f"Starting transcription service for: {file_path}")
            
            result = self.model.transcribe(file_path)
            
            text = result.get("text", "")
            language = result.get("language", "unknown")
            
            logger.info(f"Transcription complete. Language: {language}")
            
            return {
                "success" : True,
                "text" : text,
                "language" : language,
                "duration" : result.get("duration", 0)
            }
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            
            return {
                "success" : False,
                "error" : str(e),
                "text" : None
            }
    

# Global instance
_transcriber = None

def get_transcriber():
    """
    Get or create the singleton instance of TranscriptionService.
    
    This function implements the singleton pattern, ensuring that only one
    instance of TranscriptionService is created and reused throughout the
    application. This is important because loading the Whisper model is
    computationally expensive (large file size and processing time).
    
    Returns:
        TranscriptionService: The singleton instance of the transcription service.
    
    Example:
        transcriber = get_transcriber()
        result = transcriber.transcribe_audio('audio.mp3')
    """
    global _transcriber
    if _transcriber is None:
        _transcriber = TranscriptionService()
    return _transcriber
        