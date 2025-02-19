"""
local_llm.py

Defines a LocalLLM class that wraps Ollama's 'chat' functionality,
so you can import LocalLLM and use it in other scripts.
"""

import ollama

class LocalLLM:
    def __init__(self, model_name: str = "llama3.2:3b"):
        """
        :param model_name: The model name as recognized by Ollama.
                          E.g. 'llama3.2:3b', etc.
        """
        self.model_name = model_name
        print(f"Initialized LocalLLM with model: {self.model_name}")

    def chat(self, user_input: str) -> str:
        """
        Sends the user's message to the Ollama model and returns the assistant's response.
        """
        response = ollama.chat(
            model=self.model_name,
            messages=[
                {'role': 'user', 'content': user_input},
            ]
        )
        # Safely return the content, in case of unusual response structure
        return response.get("message", {}).get("content", "")
