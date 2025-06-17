import os
from datetime import datetime
from typing import Dict, Any

from .base_embeddor import BaseFileEmbeddor

class TextFileEmbeddor(BaseFileEmbeddor):
    """
    A concrete implementation for handling plain text-based files.
    """
    
    def can_handle(self, file_path: str) -> bool:
        """
        Handles common text, code, and data file extensions.
        """
        # A list of file extensions that can be treated as plain text.
        text_extensions = {'.txt', '.md', '.json', '.csv', '.py', '.js', '.html', '.css'}
        # Check if the file's extension is in our list of text extensions.
        _, ext = os.path.splitext(file_path)
        return ext.lower() in text_extensions

    def extract_content(self, file_path: str) -> str:
        """
        Reads the entire content of a text file into a string.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")
            return ""

    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extracts basic file system metadata.
        """
        try:
            # Get file stats
            stat = os.stat(file_path)
            # Get file extension
            _, ext = os.path.splitext(file_path)
            
            return {
                "source": file_path,
                "file_size": stat.st_size,
                "creation_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modification_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "file_type": ext.lower()
            }
        except Exception as e:
            print(f"Error extracting metadata for {file_path}: {e}")
            return {"source": file_path, "error": str(e)}