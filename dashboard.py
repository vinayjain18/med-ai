import streamlit as st

# st.set_page_config(page_title="AI Health Assistant Dashboard", layout="wide")

# Header
st.title("🩺 MedAI - Your AI Health Assistant")
st.divider()

# Main content
# col1, col2 = st.columns([2, 1])

st.markdown("""
## Your Personal Health Companion

This AI-powered health assistant is designed to support you in understanding and managing your health. Here's what you can do:

1. **Analyze Medical Reports**: Upload and get insights from your medical reports.
2. **Chat with AI Doctor**: Ask health-related questions and get informative responses.
3. **Learn About Diseases**: Explore information on various diseases, symptoms, and preventive measures.

Remember, while our AI assistant provides valuable information, it's not a substitute for professional medical advice. Always consult with a healthcare provider for personal medical concerns.
""")

# Quick access buttons
st.subheader("Quick Access")
col_button1, col_button2 = st.columns(2)
with col_button1:
    if st.button("📊 Analyze Reports", use_container_width=True):
        st.switch_page("report_analyzer.py")
with col_button2:
    if st.button("💬 Chat with AI", use_container_width=True):
        st.switch_page("ai_chatbot.py")

# with col2:
#     st.image("ai-doctor.webp", caption="Your AI Health Assistant", use_column_width=True)

# Additional Information
st.divider()
st.subheader("How It Works")
tab1, tab2, tab3 = st.tabs(["Report Analysis", "AI Chat", "Health Information"])

with tab1:
    st.write("Upload your medical reports and our AI will analyze them, providing you with easy-to-understand insights and highlighting key information.")

with tab2:
    st.write("Engage in a conversation with our AI doctor. Ask questions about health conditions, symptoms, or general wellness advice.")

with tab3:
    st.write("Access a wealth of health information. Learn about various diseases, their symptoms, risk factors, and preventive measures.")

# Disclaimer
st.divider()
st.caption("""
**Disclaimer**: This AI health assistant is for informational purposes only. It does not provide medical advice, diagnosis, or treatment. 
Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
""")