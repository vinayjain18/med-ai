import streamlit as st

st.sidebar.image("ai-doctor.webp")
home = st.Page("dashboard.py", title="Dashboard", icon="🏠")
report_analyzer = st.Page("report_analyzer.py", title="Report Analysis", icon="🔬")
ai_chatbot = st.Page("ai_chatbot.py", title="Health Assistant", icon="💬")

pg = st.navigation([home, report_analyzer, ai_chatbot])

st.sidebar.write('Made by [Vinay Jain](https://x.com/vinayjn18)')
pg.run()