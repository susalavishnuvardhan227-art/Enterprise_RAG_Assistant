
from pathlib import Path

from document_loader import extract_pdf_text
from chunker import create_chunks
from embedding_generator import generate_embeddings
from vector_database import store_chunks


def ingest_pdf(pdf_path):

    pdf_path = Path(pdf_path)

    # Step 1: Extract PDF text
    pages = extract_pdf_text(str(pdf_path))

    all_chunks = []

    # Step 2: Create chunks
    for page in pages:

        chunks = create_chunks(page["text"])

        for chunk_number, chunk in enumerate(chunks, start=1):

            all_chunks.append({
                "source": pdf_path.name,
                "page": page["page"],
                "chunk_number": chunk_number,
                "text": chunk
            })

    if not all_chunks:
        print(f"No readable text found in {pdf_path.name}")
        return

    # Step 3: Generate embeddings
    texts = [chunk["text"] for chunk in all_chunks]

    embeddings = generate_embeddings(texts)

    # Step 4: Store in ChromaDB
    store_chunks(all_chunks, embeddings)

    print(f"\nSuccessfully processed: {pdf_path.name}")
    print("Pages:", len(pages))
    print("Chunks:", len(all_chunks))


def ingest_folder(folder_path):

    pdf_files = list(Path(folder_path).glob("*.pdf"))

    if not pdf_files:
        print("No PDF documents found.")
        return

    print("PDF documents found:", len(pdf_files))

    for pdf_file in pdf_files:

        ingest_pdf(pdf_file)


if __name__ == "__main__":

    folder = "data/sample_documents"

    ingest_folder(folder)
