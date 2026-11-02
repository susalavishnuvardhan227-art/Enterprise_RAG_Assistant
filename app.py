
import streamlit as st
from pathlib import Path


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. PROJECT CONFIGURATION
# ==================================================

DATA_FOLDER = Path("data/sample_documents")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


# ==================================================
# 3. CUSTOM CSS
# ==================================================

st.markdown("""
<style>

    .stApp {
        background-color: #F5F7FB;
    }

    [data-testid="stSidebar"] {
        background-color: #14243A;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .main-title {
        color: #172B4D;
        font-size: 30px;
        font-weight: 700;
    }

    .subtitle {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .metric-card {
        background-color: white;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #E5EAF2;
        min-height: 115px;
    }

    .metric-label {
        color: #64748B;
        font-size: 14px;
    }

    .metric-value {
        color: #172B4D;
        font-size: 27px;
        font-weight: 700;
        margin-top: 8px;
    }

    .section-heading {
        color: #172B4D;
        font-size: 20px;
        font-weight: 600;
    }

    div[data-testid="stFileUploader"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E5EAF2;
    }

    div[data-testid="stExpander"] {
        background-color: white;
        border: 1px solid #E5EAF2;
        border-radius: 10px;
    }

    div.stButton > button[kind="primary"] {
        background-color: #2563EB;
        border: none;
        color: white;
        border-radius: 7px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# ==================================================
# 4. SESSION STATE
# ==================================================

if "search_result" not in st.session_state:
    st.session_state.search_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""


# ==================================================
# 5. SIDEBAR NAVIGATION
# ==================================================

st.sidebar.title("📚 Enterprise RAG")
st.sidebar.caption("AI Knowledge Management Platform")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Knowledge Base",
        "Knowledge Search",
        "Evaluation Centre",
        "System Settings"
    ]
)

st.sidebar.divider()

st.sidebar.caption("LOCAL ENVIRONMENT")
st.sidebar.caption("Enterprise RAG Assistant")
st.sidebar.caption("Version 1.0")


# ==================================================
# 6. HELPER FUNCTIONS
# ==================================================

def get_pdf_files():

    return sorted(
        DATA_FOLDER.glob("*.pdf"),
        key=lambda file: file.name.lower()
    )


def get_indexed_chunk_count():

    try:

        from vector_database import collection

        return collection.count()

    except Exception:

        return 0


def render_document_sources(sources):

    if not sources:

        st.info("No supporting document passages were retrieved.")
        return

    st.markdown("### Document Sources")

    st.caption(
        "The following passages were retrieved from your documents "
        "to help generate this answer."
    )

    for source in sources:

        filename = source.get("source", "Unknown document")
        page_number = source.get("page", "Unknown")

        evidence = source.get("evidence", "")

        with st.expander(
            f"📄 {filename}  ·  Page {page_number}",
            expanded=False
        ):

            st.markdown("**Relevant document extract**")

            if evidence:

                st.write(evidence)

            else:

                st.caption("No evidence text available.")


def render_search_performance(metrics):

    if not metrics:
        return

    with st.expander("Search Performance"):

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Retrieval Time",
            f"{metrics.get('retrieval_time', 0):.2f} sec"
        )

        col2.metric(
            "Generation Time",
            f"{metrics.get('generation_time', 0):.2f} sec"
        )

        col3.metric(
            "Total Time",
            f"{metrics.get('total_time', 0):.2f} sec"
        )


# ==================================================
# 7. OVERVIEW PAGE
# ==================================================

if page == "Overview":

    st.markdown(
        '<div class="main-title">Knowledge Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Monitor documents, retrieval activity and AI system performance.'
        '</div>',
        unsafe_allow_html=True
    )

    pdf_files = get_pdf_files()

    document_count = len(pdf_files)

    chunk_count = get_indexed_chunk_count()

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "Indexed Chunks", str(chunk_count)),
        (col2, "PDF Documents", str(document_count)),
        (col3, "Evaluation Tests", "4"),
        (col4, "Language Model", "Qwen 2.5")
    ]

    for column, label, value in metrics:

        with column:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    st.subheader("System Overview")

    left, right = st.columns(2)

    with left:

        st.markdown("### Document Processing")

        st.info(
            "PDF extraction, text chunking, "
            "embedding generation and vector storage."
        )

    with right:

        st.markdown("### AI Infrastructure")

        st.success("Embedding Model: all-MiniLM-L6-v2")
        st.success("Vector Database: ChromaDB")
        st.success("Language Model: Qwen 2.5 3B")

    st.write("")
    st.divider()

    st.subheader("Recent Documents")

    if pdf_files:

        for pdf_file in pdf_files[:5]:

            st.write(f"📄 {pdf_file.name}")

    else:

        st.info("No documents uploaded yet.")

    st.caption(
        "Evaluation test count reflects the current four-test "
        "development dataset, not a live quality score."
    )


# ==================================================
# 8. KNOWLEDGE BASE PAGE
# ==================================================

elif page == "Knowledge Base":

    st.title("Knowledge Base")

    st.caption(
        "Upload, process and manage enterprise PDF documents."
    )

    st.divider()

    st.subheader("Upload Documents")

    uploaded_files = st.file_uploader(
        "Select PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button(
        "Process Documents",
        type="primary"
    ):

        if not uploaded_files:

            st.warning("Please upload at least one PDF document.")

        else:

            from ingest import ingest_pdf

            progress = st.progress(0)

            total_files = len(uploaded_files)

            successful_files = 0

            for index, uploaded_file in enumerate(uploaded_files):

                safe_filename = Path(uploaded_file.name).name

                file_path = DATA_FOLDER / safe_filename

                try:

                    with open(file_path, "wb") as file:

                        file.write(uploaded_file.getbuffer())

                    with st.spinner(
                        f"Processing {safe_filename}..."
                    ):

                        ingest_pdf(file_path)

                    successful_files += 1

                    st.success(
                        f"{safe_filename} processed successfully."
                    )

                except Exception as error:

                    st.error(
                        f"Failed to process {safe_filename}: {error}"
                    )

                progress.progress((index + 1) / total_files)

            st.success(
                f"Processing completed: {successful_files}/{total_files} "
                "documents processed successfully."
            )

    st.divider()

    st.subheader("Available Documents")

    pdf_files = get_pdf_files()

    if pdf_files:

        st.write(f"Total PDF files: **{len(pdf_files)}**")

        for pdf_file in pdf_files:

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(f"📄 {pdf_file.name}")

            with col2:

                st.caption("PDF document")

    else:

        st.info(
            "No PDF documents available. Upload a document to begin."
        )

    st.divider()

    st.subheader("Database Information")

    st.metric(
        "Total Indexed Chunks",
        get_indexed_chunk_count()
    )

    st.caption("Storage: database/chroma_db")


# ==================================================
# 9. KNOWLEDGE SEARCH PAGE
# ==================================================

elif page == "Knowledge Search":

    st.title("Knowledge Search")

    st.caption(
        "Find information from your indexed enterprise documents."
    )

    st.divider()

    with st.form("knowledge_search_form"):

        question = st.text_input(
            "Enter your question",
            placeholder=(
                "Example: Which programming languages are mentioned?"
            )
        )

        search_button = st.form_submit_button(
            "Search Knowledge",
            type="primary",
            use_container_width=True
        )

    if search_button:

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            try:

                from rag_engine import generate_answer

                with st.spinner(
                    "Searching documents and generating answer..."
                ):

                    result = generate_answer(question.strip())

                # Check the expected structured response
                if not isinstance(result, dict):

                    raise TypeError(
                        "Unexpected response from rag_engine.py. "
                        "Use the updated structured-result version."
                    )

                if "answer" not in result or "sources" not in result:

                    raise ValueError(
                        "The RAG engine response is missing answer or sources."
                    )

                st.session_state.search_result = result

                st.session_state.last_question = question.strip()

            except Exception as error:

                st.session_state.search_result = None

                st.error(
                    f"Unable to generate answer: {error}"
                )

    # Display saved search result
    if st.session_state.search_result is not None:

        result = st.session_state.search_result

        st.divider()

        st.markdown("### AI Answer")

        st.markdown(result["answer"])

        st.divider()

        # Display user-friendly source references
        render_document_sources(result["sources"])

        st.divider()

        # Keep technical timings separate
        render_search_performance(
            result.get("metrics", {})
        )

    st.info(
        "Answers are generated using retrieved passages from "
        "your indexed documents and the local Qwen language model."
    )


# ==================================================
# 10. EVALUATION CENTRE PAGE
# ==================================================

elif page == "Evaluation Centre":

    st.title("Evaluation Centre")

    st.caption(
        "Evaluate document retrieval performance."
    )

    st.divider()

    st.subheader("Current Evaluation Dataset")

    st.write("Number of test questions: 4")

    st.write("Evaluation method: Expected keyword matching")

    st.info(
        "Your previous evaluation achieved 4 passes out of 4 tests "
        "(100% keyword coverage). This is a small custom test result, "
        "not a measure of overall RAG accuracy."
    )

    st.divider()

    st.subheader("Planned Evaluation Metrics")

    st.write("- Retrieval Precision")
    st.write("- Retrieval Recall")
    st.write("- Answer Faithfulness")
    st.write("- Answer Relevance")
    st.write("- Citation Coverage")
    st.write("- Response Time")

    st.caption(
        "These metrics will be implemented in a future development stage."
    )


# ==================================================
# 11. SYSTEM SETTINGS PAGE
# ==================================================

elif page == "System Settings":

    st.title("System Settings")

    st.caption(
        "View the configuration of your Enterprise RAG Assistant."
    )

    st.divider()

    st.subheader("AI Models")

    st.write("**Embedding Model:** all-MiniLM-L6-v2")

    st.write("**Language Model:** Qwen 2.5 3B")

    st.write("**Model Runtime:** Ollama")

    st.divider()

    st.subheader("Vector Database")

    st.write("**Database:** ChromaDB")

    st.write("**Collection:** enterprise_documents_v2")

    st.write("**Storage Location:** database/chroma_db")

    st.divider()

    st.subheader("Application")

    st.write("**Frontend:** Streamlit")

    st.write("**Programming Language:** Python")

    st.write("**Environment:** Local Development")

    st.info(
        "Advanced configuration, user permissions and security "
        "settings will be added in future stages."
    )


# ==================================================
# 12. FOOTER
# ==================================================

st.sidebar.divider()

st.sidebar.caption(
    "Enterprise RAG Assistant © 2026"
)
