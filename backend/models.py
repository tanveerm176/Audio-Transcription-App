from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

# Declare database models using SQLAlchemy ORM
Base = declarative_base()

class Recording(Base):
    """
    SQLAlchemy ORM model representing an audio recording in the database.
    
    This class maps to the 'recordings' table in SQLite and stores metadata
    about audio files including transcription results, timestamps, and status
    information.
    
    Attributes:
        id (str): Unique identifier for the recording (primary key).
        file_name (str): System-generated filename used for storing the audio file.
        original_filename (str): Original filename provided by the user.
        transcript (str): The text transcription of the audio content.
        duration (str): Length of the audio file in HH:MM:SS format (default: "0:00").
        date_created (datetime): Timestamp when the recording was created in UTC.
        status (str): Current state of the recording (e.g., "completed", "failed").
        error_message (str): Optional error description if transcription failed.
    """
    
    __tablename__ = "recordings"
    
    id = Column(String, primary_key=True)
    file_name = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    transcript = Column(Text, nullable=False)
    duration = Column(String, default="0:00")
    date_created = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="completed")
    error_message = Column(String, nullable=True)
    
    def __repr__(self):
        """
        Returns a string representation of the Recording instance.
        
        Returns:
            str: A formatted string containing the word "Recording" and the original filename.
        """
        return f"Recording {self.original_filename}"