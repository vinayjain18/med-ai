from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
import streamlit as st
import tempfile

load_dotenv()

# loader = PyPDFLoader("Report.pdf")
# report = loader.load_and_split()
# print(report)

system_prompt = """Act as a medical assistant with 15 years of experience reading and analyzing different medical reports like blood reports, biochemistry reports, blood sugar reports, and many more. I want you to analyze and give a detailed description of the given report. If the report contains multiple sub-reports, then break down your analysis report-wise.

Focus only on the relevant information that is critical or useful for the person or doctor. Do not provide details that are unnecessary or not actionable. Highlight any abnormal conditions and provide precautions and suggestions on how to normalize those values. If a parameter is missing, unclear, or the report type is not recognized, note this and avoid speculation.

Explain the report in a way that is understandable even to a non-doctor, avoiding complex medical jargon unless necessary. If something is not within your expertise, or if the report is not a medical report, reply with 'Sorry, but I'm a Medical assistant and can help you analyze medical reports.' and nothing else.

The report is this - {report}

Avoid hallucinations and provide accurate and appropriate responses only.

Now, go ahead and give a detailed analysis and description for each parameter/value in the report, along with suggestions for any abnormal values for each report. Conclude with a brief summary of key findings and recommended next steps. Directly start from the report without saying anything else.
"""

# st.set_page_config("Medical Report Analyzer")

st.title("Medical Report Analyzer")
st.write("Upload your medical report below to get detailed analysis and suggestions on any abnormal values.")
st.divider()
uploaded_file = st.file_uploader("Upload your report:", type=['pdf'], help="Make sure the report is in pdf format")

template = PromptTemplate.from_template(system_prompt)

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)

output_parser = StrOutputParser()

chain = template | llm | output_parser
# print(chain.invoke({'report': report}))

if uploaded_file is not None:
    with st.spinner("Analyzing your report..."):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            # Write the uploaded file data to the temporary file
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # Use PyPDFLoader to load the PDF
            loader = PyPDFLoader(tmp_file_path)
            pages = loader.load()

            st.write(chain.invoke({'report': pages}))

        finally:
            # Clean up the temporary file
            os.unlink(tmp_file_path)
