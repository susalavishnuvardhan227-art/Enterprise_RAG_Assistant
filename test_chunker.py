
from document_loader import extract_pdf_text
from chunker import create_chunks

pdf_path = "data/sample_documents/sample.pdf"

pages = extract_pdf_text(pdf_path)

all_chunks = []

for page in pages:

    chunks = create_chunks(page["text"])

    for chunk_number, chunk in enumerate(chunks, start=1):

        all_chunks.append({
            "page": page["page"],
            "chunk_number": chunk_number,
            "text": chunk
        })

print("Total chunks created:", len(all_chunks))

for chunk in all_chunks:

    print("\n------------------------")
    print("Page:", chunk["page"])
    print("Chunk:", chunk["chunk_number"])
    print("Text:", chunk["text"][:200])
