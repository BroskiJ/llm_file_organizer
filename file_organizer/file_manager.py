import os
import shutil

class FileManager:
    """
    Handles safe and restricted file system operations.
    Enforces a "no-delete" policy.
    """

    def file_exists(self, path: str) -> bool:
        """Checks if a file or directory exists at the given path."""
        return os.path.exists(path)

    def create_folder(self, path: str):
        """
        Safely creates a new folder (and any parent folders).
        Does nothing if the folder already exists.
        """
        try:
            # exist_ok=True prevents an error if the directory already exists
            os.makedirs(path, exist_ok=True)
            print(f"Ensured folder exists: {path}")
        except OSError as e:
            print(f"Error creating folder {path}: {e}")

    def move_file(self, src_path: str, dest_path: str):
        """
        Safely moves a file, but ONLY if the destination folder already exists.
        """
        if not self.file_exists(src_path):
            print(f"Error: Source file not found at {src_path}")
            return

        # --- UPDATED LOGIC ---
        # Get the destination folder from the full destination path.
        dest_folder = os.path.dirname(dest_path)

        # Check if the destination folder exists instead of creating it.
        if not self.file_exists(dest_folder):
            print(f"Error: Destination folder does not exist at '{dest_folder}'. Action aborted.")
            return
        # ---------------------

        try:
            shutil.move(src_path, dest_path)
            print(f"Successfully moved '{src_path}' to '{dest_path}'")
        except Exception as e:
            print(f"Error moving file: {e}")