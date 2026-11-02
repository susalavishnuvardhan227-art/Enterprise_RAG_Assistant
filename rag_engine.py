
import time
import ollama

from search import search_documents


MODEL_NAME = "qwen2.5:3b"

NO_ANSWER = (
    "I couldn't find this information in the indexed documents."
)


def build_sources(retrieved_chunks):
    """
    Preserve the original retrieved text as evidence.

    This avoids losing relevant information through
    overly restrictive line-based evidence extraction.
    """

    grouped_sources = {}

    for chunk in retrieved_chunks:

        source = chunk.get("source", "Unknown document")
        page = chunk.get("page", 0)
        text = chunk.get("text", "").strip()

        if not text:
            continue

        key = (source, page)

        if key not in grouped_sources:
            grouped_sources[key] = []

        if text not in grouped_sources[key]:
            grouped_sources[key].append(text)

    sources = []

    for (source, page), evidence_list in grouped_sources.items():

        sources.append({
            "source": source,
            "page": page,
            "evidence": "\n\n".join(evidence_list)[:2000]
        })

    return sources


def build_context(retrieved_chunks):
    """
    Prepare retrieved document chunks for the LLM.
    Keep source and page information with each chunk.
    """

    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):

        context_parts.append(
            f"""
DOCUMENT CHUNK {index}
Source: {chunk.get("source", "Unknown")}
Page: {chunk.get("page", "Unknown")}
Content:
{chunk.get("text", "")}
"""
        )

    return "\n".join(context_parts)


def build_prompt(question, context):
    """
    Create instructions for grounded answers,
    multiple-part questions and accurate counting.
    """

    return f"""
You are an Enterprise Document Assistant.

Your job is to answer questions using ONLY the
provided document context.

STRICT RULES:

1. Use only facts explicitly supported by the context.

2. Never invent names, dates, numbers, skills,
   qualifications, experience or policies.

3. If the question has multiple parts, answer
   each part separately.

4. Do not ignore any part of the question.

5. Preserve categories and headings used in the
   original document.

6. Do not combine different categories.

7. When asked about programming skills, distinguish
   between:
   - Programming languages
   - Data analysis tools
   - Libraries and frameworks
   - Tools and platforms
   - Databases

8. When asked to count internships:
   - Count entries explicitly identified as Intern
     or Internship.
   - Do not automatically count trainee positions
     as internships.
   - Count only distinct positions.
   - Do not count the same position twice.

9. If the context does not contain enough information
   to answer a question, say exactly:

   "{NO_ANSWER}"

10. If only one part of a multi-part question is
    supported, answer that part and clearly state
    that the other information was not found.

11. Keep answers simple, direct and well organised.

12. Never use outside knowledge.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""


def normalize_no_answer(answer):
    """
    Normalize common expressions indicating
    that the requested information was not found.
    """

    no_answer_phrases = [
        "i couldn't find this information",
        "i could not find this information",
        "not mentioned in the document",
        "not provided in the document",
        "information is not available",
        "not found in the document",
        "not available in the provided context"
    ]

    answer_lower = answer.lower()

    if any(
        phrase in answer_lower
        for phrase in no_answer_phrases
    ):
        return NO_ANSWER

    return answer


def generate_answer(question):

    start_time = time.time()

    # STEP 1: Retrieve relevant document chunks.
    retrieval_start = time.time()

    retrieved_chunks = search_documents(
        question,
        number_of_results=5,
        debug=True
    )

    retrieval_time = time.time() - retrieval_start

    # STEP 2: Handle empty retrieval.
    if not retrieved_chunks:

        return {
            "answer": NO_ANSWER,
            "sources": [],
            "metrics": {
                "retrieval_time": round(retrieval_time, 3),
                "generation_time": 0,
                "total_time": round(
                    time.time() - start_time, 3
                )
            }
        }

    # STEP 3: Prepare document evidence.
    sources = build_sources(retrieved_chunks)

    context = build_context(retrieved_chunks)

    # STEP 4: Build the prompt.
    prompt = build_prompt(question, context)

    # STEP 5: Generate an answer using Ollama.
    generation_start = time.time()

    try:

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0,
                "num_predict": 350
            }
        )

        answer = response["message"]["content"].strip()

        # STEP 6: Basic no-answer normalization.
        answer = normalize_no_answer(answer)

        # Do not display irrelevant source evidence
        # when the complete answer was not found.
        if answer == NO_ANSWER:
            sources = []

    except Exception as error:

        print("\nOllama error:", error)

        answer = (
            "The document search completed, but the AI "
            "model could not generate an answer. "
            "Please check that Ollama is running and "
            f"that {MODEL_NAME} is available."
        )

        sources = []

    # STEP 7: Calculate performance metrics.
    generation_time = time.time() - generation_start

    total_time = time.time() - start_time

    # STEP 8: Return results for CLI and Streamlit.
    return {
        "answer": answer,
        "sources": sources,
        "metrics": {
            "retrieval_time": round(retrieval_time, 3),
            "generation_time": round(generation_time, 3),
            "total_time": round(total_time, 3)
        }
    }


if __name__ == "__main__":

    question = input(
        "\nAsk a question about your documents: "
    ).strip()

    if not question:

        print("Please enter a question.")

    else:

        result = generate_answer(question)

        print("\n--- ANSWER ---")
        print(result["answer"])

        print("\n--- DOCUMENT SOURCES ---")

        if result["sources"]:

            for source in result["sources"]:

                print(
                    f"\nFile: {source['source']}"
                    f"\nPage: {source['page']}"
                    f"\nRelevant evidence:\n{source['evidence']}"
                )

        else:

            print("No supporting sources displayed.")

        print("\n--- PERFORMANCE ---")

        for metric, value in result["metrics"].items():

            print(f"{metric}: {value} seconds")
