
import re

from embedding_generator import generate_embeddings
from vector_database import collection


STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "what", "which", "who", "when", "where", "why", "how",
    "do", "does", "did", "i", "me", "my", "we", "our",
    "you", "your", "and", "or", "of", "in", "on", "at",
    "to", "for", "from", "with", "about", "mentioned",
    "tell", "show", "list", "give", "explain"
}


def get_keywords(text):

    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 1
    }


def calculate_phrase_score(question, document):

    question_lower = question.lower()
    document_lower = document.lower()

    heading_matches = {
        "programming languages": "programming languages:",
        "data analysis tools": "data analysis tools:",
        "frameworks": "libraries & frameworks:"
    }

    for question_phrase, document_heading in heading_matches.items():

        if question_phrase in question_lower:
            if document_heading in document_lower:
                return 5

    return 0


def search_documents(question, number_of_results=3, debug=False):

    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    result_limit = min(
        max(number_of_results * 3, 5),
        total_chunks
    )

    question_embedding = generate_embeddings([question])

    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=result_limit,
        include=["documents", "metadatas", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        return []

    question_keywords = get_keywords(question)

    retrieved_chunks = []

    for index, document in enumerate(documents):

        if not document or index >= len(metadatas):
            continue

        metadata = metadatas[index] or {}

        document_keywords = get_keywords(document)

        matching_keywords = question_keywords.intersection(
            document_keywords
        )

        phrase_score = calculate_phrase_score(
            question,
            document
        )

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        retrieved_chunks.append({

            "source": metadata.get(
                "source",
                "Unknown document"
            ),

            "page": metadata.get("page", 0),

            "chunk_number": metadata.get(
                "chunk_number",
                0
            ),

            "text": document,

            "keyword_score": len(matching_keywords),

            "phrase_score": phrase_score,

            "distance": distance

        })

    if not retrieved_chunks:
        return []

    # Remove chunks without keyword matches when keyword matches exist.
    has_keyword_match = any(
        chunk["keyword_score"] > 0
        for chunk in retrieved_chunks
    )

    if has_keyword_match:

        retrieved_chunks = [
            chunk for chunk in retrieved_chunks
            if chunk["keyword_score"] > 0
        ]

    # If an exact heading match exists, keep only those chunks.
    exact_matches = [
        chunk for chunk in retrieved_chunks
        if chunk["phrase_score"] > 0
    ]

    if exact_matches:
        retrieved_chunks = exact_matches

    # Rank by keyword relevance and semantic distance.
    retrieved_chunks.sort(
        key=lambda chunk: (
            -chunk["keyword_score"],

            chunk["distance"]
            if chunk["distance"] is not None
            else float("inf")
        )
    )

    retrieved_chunks = retrieved_chunks[:number_of_results]

    # Debug output
    if debug:

        print("\n--- FINAL RETRIEVED CHUNKS ---")

        for chunk in retrieved_chunks:

            print("\nSource:", chunk["source"])

            print("Page:", chunk["page"])

            print("Chunk:", chunk["chunk_number"])

            print("Phrase score:", chunk["phrase_score"])

            print("Keyword score:", chunk["keyword_score"])

            print("Distance:", chunk["distance"])

            print("Text:", chunk["text"])

    return retrieved_chunks
