import streamlit as st

st.set_page_config(
    page_title="BioBrief AI",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 BioBrief AI")

st.subheader("AI-powered Scientific Intelligence")

topic = st.text_input(
    "Enter a disease, drug, gene or biomarker",
    placeholder="Example: GLP-1 obesity"
)

if st.button("Analyze Literature"):

    st.success(f"Searching PubMed for: {topic}")

    st.info("🚧 PubMed search coming next...")
