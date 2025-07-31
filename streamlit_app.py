import streamlit as st
from phi_app import eligibility_agent, impact_agent, scoring_agent
from utils.parser import extract_text_from_file

st.set_page_config(page_title="Grant Application Evaluator", layout="wide")
st.title("📝 Grant Application Evaluator for NGOs")

uploaded_file = st.file_uploader("Upload a Grant Proposal (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    text = extract_text_from_file(uploaded_file)

    st.subheader("📄 Proposal Preview")
    st.text_area("Extracted Content", value=text[:3000], height=300)

    if st.button("Evaluate Grant Proposal"):
        with st.spinner("Checking Eligibility..."):
            eligibility_response = eligibility_agent.run(text)
        with st.spinner("Evaluating Impact..."):
            impact_response = impact_agent.run(text)
        with st.spinner("Scoring the Application..."):
            score_response = scoring_agent.run(text)

        st.success("✅ Evaluation Complete")

        # Extracting clean content only
        eligibility_text = eligibility_response.content
        impact_text = impact_response.content
        score_text = score_response.content

        final_output = f"""## ✅ Eligibility Check\n{eligibility_text}\n\n---\n\n## 🌟 Impact Evaluation\n{impact_text}\n\n---\n\n## 🏋️ Final Scoring\n{score_text}"""
        st.markdown(final_output)