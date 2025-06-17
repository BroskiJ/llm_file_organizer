import os
import argparse
import shutil # New import for deleting directories
from file_organizer.rag_system import RAGSystem
from file_organizer.embeddors.embeddor_registry import EmbeddorRegistry
from file_organizer import config 

def process_and_ingest(directory_path: str, rag_system: RAGSystem, registry: EmbeddorRegistry):
    """
    Scans a directory, processes all supported files, and ingests them into the RAG system.
    """
    print(f"\n--- Scanning Directory: {directory_path} ---")
    
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            embeddor = registry.get_embeddor_for_file(file_path)
            
            if embeddor:
                print(f"  Processing: {file_path}")
                documents, metadatas, ids = embeddor.prepare_for_embedding(file_path)
                
                if documents:
                    rag_system.ingest_documents(documents, metadatas, ids)

def main():
    """
    Main function to parse arguments and orchestrate the knowledge base build.
    """
    parser = argparse.ArgumentParser(
        description="Build or update the knowledge base by scanning specified directories."
    )
    parser.add_argument(
        'directories', 
        metavar='DIR', 
        type=str, 
        nargs='*',
        help='One or more directory paths to scan. If none are provided, uses default directories from config.'
    )
    # --- NEW: Optional flag to wipe the database before building ---
    parser.add_argument(
        '--fresh-build',
        action='store_true', # This makes it a flag that doesn't need a value (e.g., --fresh-build)
        help='If set, deletes the existing knowledge base before building a new one.'
    )
    
    args = parser.parse_args()

    # --- NEW: Logic to handle the --fresh-build flag ---
    # This happens before the RAGSystem is initialized to avoid file lock issues.
    if args.fresh_build:
        db_path = config.CHROMA_PERSIST_DIRECTORY
        if os.path.exists(db_path):
            print("--- Deleting existing knowledge base for a fresh build... ---")
            shutil.rmtree(db_path)
            print("--- Knowledge base deleted. ---")
    # ----------------------------------------------------
    
    if args.directories:
        dirs_to_process = args.directories
        print(f"Processing specified directories: {dirs_to_process}")
    else:
        dirs_to_process = config.DEFAULT_KNOWLEDGE_DIRECTORIES
        print(f"No directories specified. Processing default directories from config:\n{dirs_to_process}")
    
    rag = RAGSystem()
    registry = EmbeddorRegistry()
    
    for directory in dirs_to_process:
        if os.path.isdir(directory):
            process_and_ingest(directory, rag, registry)
        else:
            print(f"Warning: '{directory}' is not a valid directory. Skipping.")
            
    print("\n--- Knowledge base build/update process complete. ---")

if __name__ == "__main__":
    main()