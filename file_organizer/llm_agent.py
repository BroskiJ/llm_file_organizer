import ollama
from . import config

class LLMAgent:
    """
    The decision-making module that uses the Gemma LLM via Ollama.
    """
    def __init__(self):
        """
        Initializes the LLM agent by setting up the Ollama client.
        """
        self.client = ollama.Client(host=config.OLLAMA_HOST)
        self.model = config.OLLAMA_MODEL
        print(f"LLM Agent initialized to use model '{self.model}' at {config.OLLAMA_HOST}")
    
    def decide_action(self, file_info: dict, rag_context: dict):
        """
        Leverages the LLM to decide on a file organization action. 
        """
        prompt = self._build_prompt(file_info, rag_context)
        print("\n--- Sending the Following Prompt to LLM ---")
        print(prompt)
        print("--------------------------")

        try:
            response = self.client.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            # The agent's response is parsed to extract the command 
            return response['message']['content']
        except Exception as e:
            return f"Error communicating with Ollama: {e}"

    def _build_prompt(self, file_info: dict, rag_context: dict) -> str:
        """
        Constructs the prompt for the LLM with file info and RAG context. 
        """
        # Access the documents, metadata, and distances.
        retrieved_docs = rag_context['documents'][0]
        retrieved_metadatas = rag_context['metadatas'][0]
        retrieved_distances = rag_context['distances'][0]

        # Create a more informative bullet point for each result.
        bullet_points = []
        for doc, meta, dist in zip(retrieved_docs, retrieved_metadatas, retrieved_distances):
            # Safely get the source path from the metadata.
            source_path = meta.get('source', 'Unknown location')
            # Add the distance score, formatted to 4 decimal places, to the prompt.
            bullet_points.append(f'- Content: "{doc}"\n  (from file: "{source_path}", distance: {dist:.4f})')

        context_str = "\n\n".join(bullet_points) # Use double newlines to separate entries
        
        # Load the prompt template from the config file.
        prompt_template = config.AGENT_PROMPT_TEMPLATE
        
        # Populate the template with the dynamic data using .format()
        prompt = prompt_template.format(
            file_name=file_info['name'],
            file_content=file_info['content'],
            rag_context=context_str
        )
        return prompt

if __name__ == '__main__':
    # This block runs only when the script is executed directly
    
    # 1. Initialize the agent
    agent = LLMAgent()

    # 2. Create mock data to simulate what the RAG system would provide
    mock_file_info = {
        "name": "q2_earnings_call_summary.txt",
        "content": "Summary of the second quarter earnings call, focusing on growth in the enterprise sector."
    }
    mock_rag_context = {
        'documents': [['Existing file: C:\\Users\\Elijah\\Documents\\Financials\\2025_Q1_earnings.txt']]
    }

    # 3. Call the decision method with the mock data
    # This tests the agent's ability to process inputs and query the LLM.
    suggestion = agent.decide_action(
        file_info=mock_file_info,
        rag_context=mock_rag_context
    )

    # 4. Print the result from the LLM
    print("\n--- LLM Suggested Action ---")
    print(suggestion)
    print("----------------------------")