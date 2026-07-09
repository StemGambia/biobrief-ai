import streamlit as st
from Bio import Entrez
from google import genai
from agents.planner import create_plan

# ---------------------------------
# Configuration
# ---------------------------------

st.set_page_config(
    page_title="BioBrief AI",
    page_icon="🧬",
    layout="wide"
)

Entrez.email = st.secrets["PUBMED_EMAIL"]

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# ---------------------------------
# Agent Stubs (v0.2)
# ---------------------------------

def mission_controller(user_goal):
    return {
        "mission": user_goal,
        "status": "planned"
    }


def planner(mission):
    return create_plan(
        client,
        mission["mission"]
    )


def researcher(plan):

    query = plan["searches"][0]["query"]

    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=5,
        sort="relevance"
    )

    results = Entrez.read(handle)

    ids = results["IdList"]

    handle = Entrez.efetch(
        db="pubmed",
        id=",".join(ids),
        rettype="abstract",
        retmode="text"
    )

    return handle.read(), len(ids)


def analyst(text):

    prompt = f"""
You are the Principal Scientific Intelligence Analyst
for a biotechnology executive team.

Create:

# Executive Summary

# Key Scientific Findings

# Biomarkers

# Therapeutic Implications

# Research Gaps

Scientific Literature:

{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

# ---------------------------------
# UI
# ---------------------------------

with st.sidebar:
    st.header("🤖 Agent Activity")
    st.write("🧠 Mission Controller")
    st.write("📋 Planner")
    st.write("🔍 Research Agent")
    st.write("🧬 Scientific Analyst")

st.title("🧬 BioBrief AI")

st.caption(
    "Your AI Scientific Intelligence Analyst"
)

goal = st.text_input(
    "Research Mission",
    placeholder="Evaluate the future of GLP-1 therapies for obesity"
)

if st.button("Launch Mission"):

    if goal:

        progress = st.progress(0)

        st.write("🧠 Mission Controller")
        mission = mission_controller(goal)

        progress.progress(20)

        st.write("📋 Planner")

        plan = planner(mission)

        with st.expander("View Research Plan"):
            st.json(plan)

        progress.progress(40)

        st.write("🔍 Research Agent")
        abstracts, count = researcher(plan)

        progress.progress(70)

        st.write("🧬 Scientific Analyst")
        report = analyst(abstracts)

        progress.progress(100)

        st.success(f"Mission Complete ({count} papers analyzed)")

        st.markdown(report)

        with st.expander("Source Literature"):

            st.text(abstracts)

    else:

        st.warning("Please enter a research mission.")
