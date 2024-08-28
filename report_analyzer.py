from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
import tempfile
import os
import logging
import pytesseract
from pdf2image import convert_from_path
# from dotenv import load_dotenv

# load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    api_key=st.secrets["GROQ_API_KEY"]
)

output_parser = StrOutputParser()

chain = template | llm | output_parser
# print(chain.invoke({'report': report}))

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # First, try to extract text directly using PyPDFLoader
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        text = "\n".join([page.page_content for page in pages])
        
        # If no text is extracted, use OCR
        if not text.strip():
            logger.info("OCR process....converting image data to text")
            images = convert_from_path(pdf_path)
            for image in images:
                # Convert image to string using Tesseract
                ocr_text = pytesseract.image_to_string(image, config='--psm 6')
                
                # Split the extracted text into rows (lines)
                rows = ocr_text.splitlines()
                
                # Remove empty lines and append to output
                rows = [row for row in rows if row.strip() != '']
                text += "\n".join(rows) + "\n"
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
    return text

if uploaded_file is not None:
    with st.spinner("Analyzing your report..."):
        logger.info(f"File uploaded: {uploaded_file.name}, Size: {uploaded_file.size} bytes")
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            # Write the uploaded file data to the temporary file
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # Extract text from the PDF (including OCR if necessary)
            report_text = extract_text_from_pdf(tmp_file_path)
            
            if not report_text.strip():
                st.error("Unable to extract text from the PDF. Please ensure the file is not corrupted or password-protected.")
            else:
                logger.info("Starting report analysis")
                logger.info(f"Report length: {len(report_text)} characters")
                
                st.write(chain.invoke({'report': report_text}))
                logger.info("Report analysis completed successfully")
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            st.error(f"An unexpected error occurred: {str(e)}")

        finally:
            # Clean up the temporary file
            os.unlink(tmp_file_path)
