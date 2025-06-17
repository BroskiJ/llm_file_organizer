import chromadb
from chromadb.utils import embedding_functions
# The dot before 'config' creates a relative import that works
# because both files are in the same 'file_organizer' package.
from . import config

class RAGSystem:
    """
    Manages the ChromaDB vector database for the file organization agent. 
    """
    def __init__(self):
        """
        Initializes the RAGSystem.
        """
        print("--- Initializing RAGSystem ---")

        # This client saves data to the specified directory. 
        self.client = chromadb.PersistentClient(path=config.CHROMA_PERSIST_DIRECTORY)

        # This uses the SentenceTransformer model to create embeddings locally. 
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.EMBEDDING_MODEL_NAME
        )

        # This gets or creates the collection where embeddings will be stored. 
        self.collection = self.client.get_or_create_collection(
            name=config.CHROMA_COLLECTION_NAME,
            embedding_function=self.embedding_function,
        )
        print(f"ChromaDB collection '{config.CHROMA_COLLECTION_NAME}' loaded/created.")
        print("-" * 30)
    
    def ingest_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        """
        Ingests or updates documents in the ChromaDB collection in batches.
        """
        # --- NEW: Batching Logic ---
        # ChromaDB has a max batch size. We'll process our documents in smaller chunks.
        batch_size = 4000 # A safe number well below the max limit of ~5461
        total_documents = len(documents)

        for i in range(0, total_documents, batch_size):
            # Create a slice for the current batch
            end_index = i + batch_size
            batch_docs = documents[i:end_index]
            batch_metadatas = metadatas[i:end_index]
            batch_ids = ids[i:end_index]

            try:
                # Ingest the current batch
                self.collection.upsert(
                    documents=batch_docs,
                    metadatas=batch_metadatas,
                    ids=batch_ids
                )
                print(f"Successfully ingested/updated batch {i//batch_size + 1} ({len(batch_docs)} documents).")
            except Exception as e:
                print(f"Error ingesting batch starting at index {i}: {e}")
        # -------------------------
    
    def retrieve_context(self, query: str, n_results: int = 3):
        """
        Retrieves the top n_results most relevant document snippets from the collection.
        This is the 'Retrieval' part of RAG.
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            print(f"Successfully retrieved context for query: '{query}'")
            return results
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return None

# Example of how to instantiate and use the class (for testing purposes)
if __name__ == '__main__':
    rag_system = RAGSystem()

    # --- Ingestion Step ---
    # We re-run ingestion to ensure the data is present for the test.
    # ChromaDB's upsert handles this gracefully without creating duplicates.
    sample_docs = [
        "This is a project report about artificial intelligence.",
        "A simple text file containing a grocery list: milk, bread, eggs."
    ]
    sample_metadatas = [
        {"source": "C:\\Users\\Elijah\\Documents\\report.docx", "type": "docx"},
        {"source": "C:\\Users\\Elijah\\Downloads\\list.txt", "type": "txt"}
    ]
    sample_ids = ["doc_path_report_docx", "doc_path_list_txt"]
    rag_system.ingest_documents(
        documents=sample_docs, metadatas=sample_metadatas, ids=sample_ids
    )
    print(f"Total items in collection: {rag_system.collection.count()}")
    print("-" * 30)

    # --- Retrieval Step ---
    print("Testing context retrieval...")
    # This query is semantically similar to one of our ingested documents
    query = "What are the reports about AI?"
    retrieved_results = rag_system.retrieve_context(query, n_results=1)

    if retrieved_results:
        print("\n--- Retrieved Results ---")
        for i, doc in enumerate(retrieved_results['documents'][0]):
            print(f"Result {i+1}:")
            print(f"  Document: {doc}")
            print(f"  Metadata: {retrieved_results['metadatas'][0][i]}")
            print(f"  Distance: {retrieved_results['distances'][0][i]:.4f}") # Lower distance is better
        print("------------------------")