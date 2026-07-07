import streamlit as st
from Bio import Entrez

# PubMed setup
Entrez.email = "scientistsofthegambia@gmail.com"

st.set_page_config(
    page_title="BioBrief AI",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 BioBrief AI")
st.subheader("AI-powered Scientific Intelligence")

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


def fetch_articles(pubmed_ids):

    handle = Entrez.efetch(
        db="pubmed",
        id=",".join(pubmed_ids),
        rettype="abstract",
        retmode="text"
    )

    return handle.read()


if st.button("Analyze Literature"):

    if topic:

        with st.spinner("Searching PubMed..."):

            papers = search_pubmed(topic)

            abstracts = fetch_articles(papers)

        st.success(
            f"Found {len(papers)} scientific papers"
        )

        st.text_area(
            "PubMed Results",
            abstracts,
            height=500
        )

    else:
        st.warning("Please enter a topic")
