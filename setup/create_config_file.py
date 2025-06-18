import os

# Ensure the script works from any directory by setting the working directory to the project root
os.chdir(os.path.dirname(os.path.abspath(__file__)))

CONFIG_TEMPLATE = '''
import os

# Project root directory (auto-detected)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# --- ChromaDB Settings ---
CHROMA_PERSIST_DIRECTORY = os.path.join(PROJECT_ROOT, "..", "data", "chromadb")
CHROMA_COLLECTION_NAME = "file_organization_knowledge"

# --- Embedding Model Settings ---
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# --- LLM Agent Settings ---
OLLAMA_MODEL = 'your-ollama-model-name'  # Replace with your preferred model
OLLAMA_HOST = 'http://localhost:11434'  # Change if your Ollama server runs elsewhere

AGENT_PROMPT_TEMPLATE = """
You are an expert file organization agent. Your task is to decide the best folder path for a given file based on its content and context from the existing file system.

**Constraints:**
- You can only suggest a 'move' action.
- The destination path must be a valid path structure (e.g., 'C:/Users/YourName/Documents/Reports').
- Do not suggest deleting the file.
- **You must only suggest a folder that already exists based on the file paths provided in the context.**

**File to Organize:**
- Name: {file_name}
- Content Snippet: "{file_content}"

**Relevant Context from Existing Files (from RAG search):**
{rag_context}

Based on all the information above, what is the single best destination folder for this file? Respond with only the full destination path and nothing else.
"""
'''

def create_config_file(output_path="file_organizer/config.py"):
    """
    Creates a default config.py file for the project, with placeholder values and no personal information.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(CONFIG_TEMPLATE)
    print(f"Default config.py created at: {output_path}")

if __name__ == "__main__":
    create_config_file()
