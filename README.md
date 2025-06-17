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
conda env create -f environment.yml
conda activate gemma_file_organizer
```

### 3. Configure the Project

- Edit `file_organizer/config.py` to set your model and database preferences.
- You can generate a default config file with:

```bash
python create_config_file.py
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

## File Structure

- `file_organizer/` — Core logic, embeddors, and RAG system
- `data/chromadb/` — Vector database storage
- `build_knowledge_base.py` — Script to ingest files
- `main.py` — Main entry point for file organization
- `create_config_file.py` — Generates a default config file
- `environment.yml` — Conda environment specification

## Requirements

- Python 3.10+
- Conda
- Ollama (for local LLM agent)
- ChromaDB
- LangChain

## License

MIT License

## Disclaimer

This project is for local, personal use. Do not include personal information in configuration files you share.
