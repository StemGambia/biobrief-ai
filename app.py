import streamlit as st
from Bio import Entrez
from google import genai


# -----------------------------
# Configuration
# -----------------------------

st.set_page_config(
    page_title="BioBrief AI",
    page_icon="🧬",
    layout="wide"
)

# Secrets
Entrez.email = st.secrets["PUBMED_EMAIL"]

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# -----------------------------
# App Interface
# -----------------------------

st.title("🧬 BioBrief AI")
st.subheader("AI Scientific Intelligence from PubMed")

topic = st.text_input(
    "Enter a disease, drug, gene, or biomarker",
    placeholder="Example: GLP-1 obesity"
)


# -----------------------------
# PubMed Functions
# -----------------------------

def search_pubmed(query, max_results=5):

    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results,
        sort="relevance"
    )

    results = Entrez.read(handle)

    return results["IdList"]


def fetch_articles(pubmed_ids):

    handle = Entrez.efetch(
        db="pubmed",
        id=",".join(pubmed_ids),
        rettype="abstract",
        retmode="text"
    )

    return handle.read()


# -----------------------------
# Gemini Function
# -----------------------------

def summarize_science(text):

    prompt = f"""
You are an expert biotech scientific analyst.

Analyze the PubMed abstracts below.

Create a concise scientific intelligence report with:

## Executive Summary
Summarize the most important discoveries.

## Key Scientific Findings
List the major findings.

## Biomarkers and Biological Targets
Identify important genes, proteins, pathways, or biomarkers.

## Therapeutic Implications
Discuss drugs, treatments, or clinical relevance.

## Research Gaps
Identify unanswered questions and future opportunities.

## Investment or R&D Signals
Highlight emerging areas that biotech leaders should monitor.

Use clear language suitable for biotech executives.

PubMed Literature:

{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# -----------------------------
# Main Workflow
# -----------------------------

if st.button("Generate Scientific Brief"):

    if topic:

        with st.spinner("Searching PubMed and analyzing literature..."):

            pubmed_ids = search_pubmed(topic)

            abstracts = fetch_articles(pubmed_ids)

            report = summarize_science(abstracts)


        st.success(
            f"Analyzed {len(pubmed_ids)} PubMed publications"
        )

        st.markdown("## 🧠 BioBrief Scientific Report")

        st.write(report)


        with st.expander("📄 View Source Abstracts"):

            st.text(abstracts)

    else:

        st.warning(
            "Please enter a research topic"
        )
