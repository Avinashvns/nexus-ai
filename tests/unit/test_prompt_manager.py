from llm.prompts import prompt_manager

def main():
    prompt = prompt_manager.load("system.txt")
    print(prompt)

if __name__ == "__main__":
    main()