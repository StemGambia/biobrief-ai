import streamlit as st
from Bio import Entrez
import google.generativeai as genai

# Configuration
#Entrez.email = "your_email@example.com"
Entrez.email = st.secrets["PUBMED_EMAIL"]

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

st.set_page_config(
    page_title="BioBrief AI",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 BioBrief AI")
st.subheader("AI Scientific Intelligence from PubMed")


topic = st.text_input(
    "Enter a disease, drug, gene, or biomarker",
    placeholder="Example: GLP-1 obesity"
)


def search_pubmed(query, max_results=5):

    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results,
        sort="relevance"
    )

    results = Entrez.read(handle)

    return results["IdList"]


def fetch_articles(ids):

    handle = Entrez.efetch(
        db="pubmed",
        id=",".join(ids),
        rettype="abstract",
        retmode="text"
    )

    return handle.read()


def summarize_science(text):

    prompt = f"""
You are a biotech scientific analyst.

Analyze these PubMed abstracts.

Create:

1. Executive Summary
2. Key Scientific Findings
3. Important Biomarkers or Targets
4. Therapeutic Implications
5. Research Gaps

Be concise and accurate.

Literature:
{text}
"""

    response = model.generate_content(prompt)

    return response.text


if st.button("Generate Scientific Brief"):

    if topic:

        with st.spinner("Reading scientific literature..."):

            ids = search_pubmed(topic)

            abstracts = fetch_articles(ids)

            summary = summarize_science(abstracts)


        st.success(
            f"Analyzed {len(ids)} PubMed papers"
        )

        st.markdown("## 🧠 Scientific Brief")

        st.write(summary)


        with st.expander("View Source Papers"):
            st.text(abstracts)

    else:
        st.warning("Enter a research topic")
