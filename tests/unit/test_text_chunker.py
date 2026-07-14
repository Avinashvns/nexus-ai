from rag.chunker import text_chunker
from rag.pdf_loader import pdf_loader


def main():
    content = pdf_loader.load(
        "tests/data/sample.pdf"
    )

    chunks = text_chunker.split(content)

    print(f"Total Chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {index} ---")
        print(chunk)


if __name__ == "__main__":
    main()