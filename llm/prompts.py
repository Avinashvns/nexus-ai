from pathlib import Path

class PromptManager:
    def __init__(self):
        self.prompt_dir = Path("prompts")

    
    def load(self,filename: str) -> str:
        file_path = self.prompt_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"{filename} not found.")
        
        return file_path.read_text(encoding="utf-8")

prompt_manager = PromptManager()