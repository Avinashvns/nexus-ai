from llm.client import ollama_client
from llm.prompts import prompt_manager
from configs.settings import get_settings

class LLMRouter:
    def __init__(self):
        settings = get_settings
        self.provider = "ollama"

        self.clients = {
            "ollama" : ollama_client,
            # "openai": openai_client,
            # "gemini": gemini_client,
        }
       
    
    def generate(self, prompt: str) -> str:
        system_prompt = prompt_manager.load("system.txt")

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]
        client = self.clients[self.provider]
        return client.generate(messages)

llm_router = LLMRouter()