import os

# Ensure the script works from any directory by setting the working directory to the project root
os.chdir(os.path.dirname(os.path.abspath(__file__)))

CONFIG_TEMPLATE = '''
import os

# Project root directory (auto-detected)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# --- ChromaDB Settings ---
# This sets the persistent storage location for the vector database
CHROMA_PERSIST_DIRECTORY = os.path.join(PROJECT_ROOT, "..", "data", "chromadb")
# This defines the name for the database collection. 
CHROMA_COLLECTION_NAME = "file_organization_knowledge"

# --- Embedding Model Settings ---
# This specifies the local model for creating vector embeddings. 
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# --- LLM Agent Settings ---
OLLAMA_MODEL = 'your-ollama-model-name'  # This should math a model you have pulled in Ollama.
OLLAMA_HOST = 'http://localhost:11434'  # Change if your Ollama server runs elsewhere

# This is the template for the LLM agent's prompt. This can be customized as needed to include specific instructions about user organization preferences.
AGENT_PROMPT_TEMPLATE = """
You are an expert file organization agent. Your task is to decide the best folder path for a given file based on its content and context from the existing file system.

**Constraints:**
- You can only suggest a 'move' action.
- The destination path must be a valid path structure (e.g., 'C:/Users/UserName/Documents/Reports').
- Do not suggest deleting the file.
- **You must only suggest a folder that already exists based on the file paths provided in the context.**

**File to Organize:**
- Name: {file_name}
- Content Snippet: "{file_content}"

**Relevant Context from Existing Files (from RAG search):**
{rag_context}

Based on all the information above, what is the single best destination folder for this file? Respond with only the full destination path and nothing else.
"""

# --- Default Knowledge Directories ---
# These are the directories that will be scanned for files to build the knowledge base whenever the build_knowledge_base.py script is run with no arguments.
DEFAULT_KNOWLEDGE_DIRECTORIES = [
    # Delete this comment and add your default directories here, e.g.:
    # C:/Users/UserName/Documents,
]
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
