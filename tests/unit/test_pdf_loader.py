from rag.pdf_loader import pdf_loader


def main():
    content = pdf_loader.load(
        "tests/data/sample.pdf"
    )

    print(content[:500])


if __name__ == "__main__":
    main()