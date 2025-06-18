import os
import argparse
from file_organizer.rag_system import RAGSystem
from file_organizer.llm_agent import LLMAgent
from file_organizer.file_manager import FileManager
from file_organizer.embeddors.embeddor_registry import EmbeddorRegistry

def run_organization_workflow(file_path: str, auto_confirm: bool = False):
    """
    Runs the full organization workflow for a single, specified file.
    """
    # 1. Initialize all modules
    rag = RAGSystem()
    llm = LLMAgent()
    file_manager = FileManager()
    embeddor_registry = EmbeddorRegistry()

    # 2. Check if the file exists
    if not file_manager.file_exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    # 3. Get the correct embeddor for the file and extract its content
    embeddor = embeddor_registry.get_embeddor_for_file(file_path)
    if not embeddor:
        print(f"No suitable processor for '{file_path}'. Skipping.")
        return
        
    content = embeddor.extract_content(file_path)
    
    if not content:
        print(f"Could not extract content from '{file_path}'. Skipping.")
        return

    # 4. Retrieve context from the RAG system based on the file's content
    print("\n--- Retrieving Context for New File ---")
    context = rag.retrieve_context(query=content, n_results=3)

    # 5. Use the LLM to decide on a destination
    print("\n--- Handing off to LLM Agent for Decision ---")
    file_info = {"name": os.path.basename(file_path), "content": content[:500]}
    llm_response = llm.decide_action(file_info=file_info, rag_context=context)
    suggested_folder = llm_response.strip()
    
    print(f"\n--- LLM Suggested Destination Folder ---\n{suggested_folder}")
    print("------------------------------------")

    # 6. Validate and correct the LLM's response
    _, file_extension = os.path.splitext(suggested_folder)
    if file_extension:
        print(f"Validation: LLM suggested a file path. Correcting to use its parent folder.")
        suggested_folder = os.path.dirname(suggested_folder)
        print(f"Corrected Folder: {suggested_folder}")

    # 7. Move the file to the suggested folder (and ask for confirmation)
    if suggested_folder and isinstance(suggested_folder, str) and ":" in suggested_folder:
        # Construct the full source and destination paths
        src_path = os.path.abspath(file_path)
        dest_path = os.path.join(suggested_folder, os.path.basename(file_path))

        # Get user confirmation before proceeding
        print(f"\nProposed Action: Move \n'{src_path}' \nto \n'{dest_path}'")
        if auto_confirm:
            user_confirmation = 'y'
            print("Auto-confirm enabled: proceeding without user input.")
        else:
            user_confirmation = input("Proceed with file move? [Y/N]: ")

        if user_confirmation.lower().strip() == 'y':
            print(f"\n--- Executing File Action ---")
            file_manager.move_file(src_path, dest_path)
        else:
            print("--- Action aborted by user. ---")
    else:
        print(f"\n--- Invalid destination format suggested ('{suggested_folder}'). No action taken. ---")

def main():
    """
    Main function to parse arguments and start the workflow.
    """
    parser = argparse.ArgumentParser(description="Organize a single file using an intelligent agent.")
    parser.add_argument(
        "file_path", 
        metavar="FILE_PATH", 
        type=str,
        help="The full path to the file to be organized."
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Bypass user confirmation and automatically move the file."
    )
    args = parser.parse_args()
    run_organization_workflow(args.file_path, auto_confirm=args.yes)

if __name__ == "__main__":
    main()