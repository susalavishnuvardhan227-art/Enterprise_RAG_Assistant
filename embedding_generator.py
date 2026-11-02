
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(text_chunks):

    embeddings = model.encode(text_chunks)

    return embeddings


# Test the embedding model
if __name__ == "__main__":

    sentences = [
        "How can I apply for leave?",
        "What is the procedure for taking vacation?",
        "Python is a programming language."
    ]

    vectors = generate_embeddings(sentences)

    print("Embedding generation successful!")

    print("Number of sentences:", len(sentences))

    print("Vector shape:", vectors.shape)

    print("\nFirst sentence embedding:")
    print(vectors[0])
