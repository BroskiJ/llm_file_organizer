# Setup Guide for LLM File Organizer

This guide will walk you through installing, configuring, and running the LLM File Organizer project.

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd llm_file_organizer
```

## 2. Set Up the Python Environment

> **Note:** PyTorch is used by ChromaDB for GPU acceleration in this project. Ollama has its own GPU support and does not depend on PyTorch. If you do not have a compatible GPU, follow the directions in the `setup/environment.yml` file (or 'setup/requirements.txt' if using pip) to install the appropriate (CPU or GPU) version of PyTorch for your system.

### Option A: Using Conda (Recommended)

```bash
conda env create -f setup/environment.yml
conda activate llm_file_organizer
```

### Option B: Using pip

```bash
pip install -r setup/requirements.txt
```

## 3. Configure the Project

- First, generate a default config file with:

```bash
python setup/create_config_file.py
```

- Then, edit `file_organizer/config.py` to set your model and database preferences.

This will create a `file_organizer/config.py` file with default settings. You may need to update the following:

- `OLLAMA_MODEL`: The name of the model you have pulled in Ollama (e.g., 'gemma3:4b-it-qat').
- `OLLAMA_HOST`: The URL where your Ollama server is running (default is `http://localhost:11434`).
- `EMBEDDING_MODEL_NAME`: The local embedding model to use (default is 'all-MiniLM-L6-v2').
- `CHROMA_PERSIST_DIRECTORY`: Where ChromaDB will store its data (default is `data/chromadb`).

## 4. Build the Knowledge Base

The knowledge base is a vector database (ChromaDB) built from your files. To scan and ingest files:

```bash
python build_knowledge_base.py <directory1> <directory2> ...
```

- You can specify one or more directories to scan. If none are provided, the script will use default directories from your config.
- To reset the database before building, use the `--fresh-build` flag:

```bash
python build_knowledge_base.py --fresh-build <directory>
```

## 5. Organize Files

To organize a file using the LLM agent:

```bash
python main.py <file-path>
```

- The script will analyze the file, retrieve context from the knowledge base, and use the LLM to suggest a destination folder.
- You will be prompted to confirm before any file is moved.

## 6. Automate or Integrate (Optional)

### Windows

- You can automate file organization by creating your own `.bat` script and using Task Scheduler, or by adding a right-click action via the Registry Editor to send files to your script. For example:

```bat
@echo off
REM --- CONFIGURE YOUR PATHS HERE ---
set PROJECT_PATH="C:\path\to\llm_file_organizer"
set CONDA_PATH="C:\path\to\anaconda3"

REM Activate the conda environment
call %CONDA_PATH%\Scripts\activate.bat llm_file_organizer
cd /d %PROJECT_PATH%

REM Run the main python script, passing the file path as an argument
python main.py %1
```

### Mac

- Use the Shortcuts app to create a right-click (context menu) action that runs a shell script, or add custom actions using third-party tools like Service Station or Context Menu (available in the Mac App Store).
- You can also add actions to the Finder context menu using Automator or Shortcuts to run your script on selected files.

### Linux

- Add a custom action in your file manager (e.g., Nautilus, Dolphin, Thunar) to run the script on selected files. This is usually found in the file manager's preferences under 'Custom Actions' or 'Scripts'.

See your OS documentation or file manager help for details on adding context menu actions.

## 7. Project Structure

- `file_organizer/` — Core logic, embeddors, and RAG system
- `data/chromadb/` — Vector database storage
- `build_knowledge_base.py` — Script to ingest files
- `main.py` — Main entry point for file organization
- `setup/` — Environment and configuration setup scripts
  - `environment.yml` — Conda environment specification
  - `create_config_file.py` — Generates a default config file
- `file_organizer/config.py` — Project configuration (generated or edited by user)

## 8. Requirements

- Python 3.12+
- Conda (optional, for environment management)
- Ollama (for local LLM agent)
- ChromaDB
- LangChain

## 9. Troubleshooting & Tips

- **Ollama must be running** and have your chosen model pulled before you can organize files.
- If you change the embedding model or database location, rebuild the knowledge base.
- The config file can be regenerated at any time with `python setup/create_config_file.py`.
- For advanced configuration, edit `file_organizer/config.py` directly.

## 10. License & Disclaimer

MIT License

This project is for local, personal use. Do not include personal information in configuration files you share.
