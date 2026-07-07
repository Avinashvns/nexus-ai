from llm.client import ollama_client

def main():
    response = ollama_client.generate(
        "Say Hello from Nexus AI"
    )

    print(response)


if __name__=="__main__":
    main()