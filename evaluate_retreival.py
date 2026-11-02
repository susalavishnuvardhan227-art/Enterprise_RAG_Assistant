
import re

from evaluation_dataset import evaluation_data
from search import search_documents


total_tests = len(evaluation_data)
passed_tests = 0


for test in evaluation_data:

    question = test["question"]
    expected_keywords = test["expected_keywords"]

    # Step 1: Retrieve relevant document chunks
    retrieved_text = search_documents(
        question,
        number_of_results=10
    )

    # Step 2: Debug college retrieval
    if "college" in question.lower():

        print("\nDEBUG: Retrieved document text:")
        print(retrieved_text)

    # Step 3: Normalize retrieved text
    normalized_text = re.sub(
        r"\s+", " ", retrieved_text
    ).lower()

    # Step 4: Check expected keywords
    found_keywords = []

    for keyword in expected_keywords:

        normalized_keyword = re.sub(
            r"\s+", " ", keyword
        ).lower()

        if normalized_keyword in normalized_text:
            found_keywords.append(keyword)

    # Step 5: Display test results
    print("\n----------------------------")
    print("Question:", question)
    print("Expected keywords:", expected_keywords)
    print("Found keywords:", found_keywords)

    if len(found_keywords) == len(expected_keywords):

        print("Result: PASS")
        passed_tests += 1

    else:
        print("Result: FAIL")


# Step 6: Calculate evaluation score
score = (passed_tests / total_tests) * 100

print("\n============================")
print("RAG RETRIEVAL EVALUATION")
print("============================")
print("Total tests:", total_tests)
print("Passed:", passed_tests)
print("Failed:", total_tests - passed_tests)
print("Keyword coverage:", round(score, 2), "%")
