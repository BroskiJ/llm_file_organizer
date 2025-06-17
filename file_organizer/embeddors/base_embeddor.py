from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

from langchain.text_splitter import RecursiveCharacterTextSplitter

class BaseFileEmbeddor(ABC):
    """
    Abstract base class defining the interface for all file embeddors.

    This ensures that every file handler, regardless of the file type,
    provides a consistent way to extract content and metadata.
    """

    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """
        Determines if this embeddor is capable of processing the given file.
        
        Args:
            file_path: The path to the file.
            
        Returns:
            True if the file can be handled, False otherwise.
        """
        pass

    @abstractmethod
    def extract_content(self, file_path: str) -> str:
        """
        Extracts the primary text content from the file.
        
        Args:
            file_path: The path to the file.
            
        Returns:
            A string containing the extracted text content.
        """
        pass

    @abstractmethod
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extracts relevant metadata from the file.
        
        Args:
            file_path: The path to the file.
            
        Returns:
            A dictionary of metadata (e.g., author, creation date, file type).
        """
        pass

    def prepare_for_embedding(self, file_path: str) -> Tuple[List[str], List[Dict], List[str]]:
        """
        A concrete method that orchestrates extraction, chunking, and preparation.
        """
        if not self.can_handle(file_path):
            return [], [], []

        content = self.extract_content(file_path)
        if not content:
            return [], [], []
            
        base_metadata = self.extract_metadata(file_path)
        
        # --- Chunking Logic ---
        # This splitter tries to keep paragraphs/sentences together.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # The max size of each chunk (in characters)
            chunk_overlap=200   # The number of characters to overlap between chunks
        )
        chunks = text_splitter.split_text(content)
        # -------------------------

        # --- UPDATED: Prepare lists for multiple chunks ---
        documents = chunks
        metadatas = []
        ids = []

        for i, chunk in enumerate(chunks):
            # Create a unique ID for each chunk
            chunk_id = f"{file_path}-chunk-{i}"
            ids.append(chunk_id)

            # Create metadata for each chunk, linking back to the original file
            chunk_metadata = base_metadata.copy()
            chunk_metadata['chunk_number'] = i
            chunk_metadata['content_snippet'] = chunk[:100] # Add a snippet for context
            metadatas.append(chunk_metadata)
        
        return documents, metadatas, ids