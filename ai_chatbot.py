import streamlit as st
from groq import Groq
# from dotenv import load_dotenv
# import os

# load_dotenv()

st.title("Health Assistant")
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        """We appreciate your engagement! This AI assistant is designed to provide
        information on healthcare-related topics like any disease or virus, its symptoms and preventive measures. 
        Please note that it should not replace professional medical advice, diagnosis, or treatment.
        """
    )

system_prompt = """You are an doctor with 10 years of experience in solving patients disease and curing them. Your 
primary function is to provide accurate, up-to-date, and helpful information on health-related topics like any disease 
or virus, its symptoms and preventive measures. You are knowledgeable about various medical conditions, treatments, and
preventions. You are empathetic and understanding, and you will provide clear and concise answers to patients.

Don't hallucinate and if someone asked you any query outside the health domain, 
just say "Sorry, I'm an AI health assistant and can help you with any query related to healthcare".

Remember, your role is to inform and guide users towards better health understanding, always within the bounds of responsible AI assistance in healthcare.
Don't give any programming output if asked even if it's any kind of help in it.

Once again, I'm saying - Don't hallucinate and if someone asked you any query outside the health domain, 
just say "Sorry, I'm an AI health assistant and can help you with any query related to healthcare".
"""

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["groq_model"] = "gemma2-9b-it"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What health-related question do you have?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model=st.session_state["groq_model"],
                messages=st.session_state.messages,
                temperature=0.1,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            error_message = """
                Oops! Sorry, I encountered an error while processing your request.
                Please refresh the page or contact support if the issue persists.
            """
            st.session_state.messages.append(
                {"role": "assistant", "content": error_message}
            )
            st.rerun()