from .text_embeddor import TextFileEmbeddor
from .pdf_embeddor import PDFEmbeddor
# We will add future embeddors here, e.g., from .word_embeddor import WordDocumentEmbeddor

class EmbeddorRegistry:
    """
    A registry to hold and manage all concrete embeddor instances.
    """
    def __init__(self):
        """
        Initializes the registry by creating instances of all known embeddors.
        """
        self.embeddors = [
            TextFileEmbeddor(),
            PDFEmbeddor(),
            # Add new embeddor instances here
        ]
        print(f"EmbeddorRegistry initialized with {len(self.embeddors)} embeddors.")

    def get_embeddor_for_file(self, file_path: str):
        """
        Finds and returns the appropriate embeddor for a given file path.

        It iterates through the registered embeddors and returns the first one
        that reports it can handle the file type.

        Args:
            file_path: The path to the file that needs processing.

        Returns:
            An instance of a BaseFileEmbeddor subclass, or None if no
            suitable embeddor is found.
        """
        for embeddor in self.embeddors:
            if embeddor.can_handle(file_path):
                print(f"Found suitable embeddor for '{file_path}': {embeddor.__class__.__name__}")
                return embeddor
        
        print(f"No suitable embeddor found for '{file_path}'.")
        return None