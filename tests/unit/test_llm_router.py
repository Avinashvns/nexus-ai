from llm.router import llm_router

def main():
    response = llm_router.generate(
        # "What is Nexus AI?"
        "Introduce yourself in one sentence."
    )

    print(response)

if __name__ == "__main__":
    main()