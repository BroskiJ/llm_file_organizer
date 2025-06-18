# Gemma File Organizer

A smart file organization tool that uses vector embeddings and a local LLM agent to automatically organize your files based on their content and context.

## Features

- Scans directories and ingests files into a vector database (ChromaDB)
- Uses local embedding models for efficient semantic search
- Integrates with a local LLM agent (Ollama) for intelligent file organization decisions
- Supports multiple file types (text, PDF, and more)
- Easily configurable and extensible

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd gemma_file_organizer
```

### 2. Set Up the Conda Environment

```bash
conda env create -f setup/environment.yml
conda activate llm_file_organizer
```

Or, if you prefer not to use Conda, install dependencies with pip:

```bash
pip install -r setup/requirements.txt
```

> **Note:** PyTorch is used by ChromaDB for GPU acceleration in this project. Ollama has its own GPU support and does not depend on PyTorch. If you do not have a compatible GPU, follow the directions in the `setup/environment.yml` file (or 'setup/requirements.txt' if using pip) to install the appropriate (CPU or GPU) version of PyTorch for your system.

### 3. Configure the Project

- Edit `file_organizer/config.py` to set your model and database preferences.
- You can generate a default config file with:

```bash
python setup/create_config_file.py
```

### 4. Build the Knowledge Base

Scan and ingest your files:

```bash
python build_knowledge_base.py <directory1> <directory2> ...
```

Or use the `--fresh-build` flag to reset the database:

```bash
python build_knowledge_base.py --fresh-build <directory>
```

### 5. Organize Files

Run the main script to organize files using the LLM agent:

```bash
python main.py <file-path>
```

## Intended Workflow

### Windows

- You can automate file organization by creating your own `.bat` script and using Task Scheduler, or by adding a right-click action via the Registry Editor to send files to your script. For example:

```bat
@echo off
REM --- CONFIGURE YOUR PATHS HERE ---
set PROJECT_PATH="C:\path\to\gemma_file_organizer"
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

## File Structure

- `file_organizer/` — Core logic, embeddors, and RAG system
- `data/chromadb/` — Vector database storage
- `build_knowledge_base.py` — Script to ingest files
- `main.py` — Main entry point for file organization
- `setup/` — Environment and configuration setup scripts
  - `environment.yml` — Conda environment specification
  - `create_config_file.py` — Generates a default config file
- `file_organizer/config.py` — Project configuration (generated or edited by user)

## Requirements

- Python 3.12+
- Conda
- Ollama (for local LLM agent)
- ChromaDB
- LangChain

## License

MIT License

## Disclaimer

This project is for local, personal use. Do not include personal information in configuration files you share.
