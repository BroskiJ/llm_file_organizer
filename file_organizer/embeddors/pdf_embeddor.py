import os
from datetime import datetime
from typing import Dict, Any

from pypdf import PdfReader # The library we just installed
from .base_embeddor import BaseFileEmbeddor

class PDFEmbeddor(BaseFileEmbeddor):
    """
    A concrete implementation for handling PDF files.
    """

    def can_handle(self, file_path: str) -> bool:
        """
        Checks if the file has a .pdf extension.
        """
        return file_path.lower().endswith('.pdf')

    def extract_content(self, file_path: str) -> str:
        """
        Extracts the text content from all pages of a PDF file.
        """
        try:
            reader = PdfReader(file_path)
            content = []
            for page in reader.pages:
                # Extract text from each page and add it to our list
                page_text = page.extract_text()
                if page_text:
                    content.append(page_text)
            # Join the content from all pages into a single string
            return "\n".join(content)
        except Exception as e:
            print(f"Error reading PDF file {file_path}: {e}")
            return ""

    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extracts basic file system metadata and PDF-specific metadata.
        """
        metadata = {}
        try:
            # Get basic file system metadata
            stat = os.stat(file_path)
            metadata.update({
                "source": file_path,
                "file_size": stat.st_size,
                "creation_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modification_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "file_type": ".pdf"
            })

            # Get PDF-specific metadata
            reader = PdfReader(file_path)
            if reader.metadata:
                metadata.update({
                    "pdf_author": reader.metadata.author,
                    "pdf_title": reader.metadata.title,
                    "pdf_subject": reader.metadata.subject,
                    "pdf_creator": reader.metadata.creator,
                })
            return metadata
        except Exception as e:
            print(f"Error extracting metadata for {file_path}: {e}")
            # Return whatever metadata was successfully gathered before the error
            if "source" not in metadata:
                 metadata["source"] = file_path
            metadata["error"] = str(e)
            return metadata