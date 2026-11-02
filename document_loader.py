import pymupdf
def extract_pdf_text(pdf_path):
    document = pymupdf.open(pdf_path)
    extracted_pages = []
    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")
        if text.strip():
            extracted_pages.append({
                "page": page_number,
                "text": text
            })
    document.close()
    return extracted_pages
# Run this test only when executing this file directly
if __name__ == "__main__":
    pdf_path = "data/sample_documents/sample.pdf"
    pages = extract_pdf_text(pdf_path)
    print("PDF processing completed!")
    print("Total pages extracted:", len(pages))
