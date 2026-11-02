
import chromadb
import hashlib

# Create a persistent database
client = chromadb.PersistentClient(
    path="database/chroma_db"
)

# Create a new collection for the upgraded system
collection = client.get_or_create_collection(
    name="enterprise_documents_v2"
)


def store_chunks(chunks, embeddings):

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        source = chunk["source"]
        page = chunk["page"]
        chunk_number = chunk["chunk_number"]

        # Create a unique ID for each document chunk
        unique_text = f"{source}_{page}_{chunk_number}"

        chunk_id = hashlib.sha256(
            unique_text.encode()
        ).hexdigest()

        ids.append(chunk_id)

        documents.append(chunk["text"])

        metadatas.append({
            "source": source,
            "page": page,
            "chunk_number": chunk_number
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print("Chunks stored successfully!")
    print("Total stored chunks:", collection.count())


if __name__ == "__main__":

    print("ChromaDB initialized!")
    print("Collection name:", collection.name)
