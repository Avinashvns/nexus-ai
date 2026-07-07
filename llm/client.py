from ollama import Client
from tenacity import retry, stop_after_attempt, wait_fixed

from configs.settings import get_settings
from core.logger import app_logger

class OllamaClient:
    def __init__(self):
        settings = get_settings()

        self.client= Client(host=settings.ollama_host)
        self.model = settings.default_model

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def generate(self, messages: list[dict]) -> str:
        try:
            app_logger.info(f"Sending request to {self.model}")

            response = self.client.chat(
                model=self.model,
                messages=messages,
            )

            content = response["message"]["content"]

            app_logger.success("Response received")

            return content

        except Exception as e:
            app_logger.error(f"LLM Error: {e}")
            raise
        

ollama_client = OllamaClient()