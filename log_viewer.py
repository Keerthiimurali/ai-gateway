import streamlit as st
from logger import read_logs

st.title("AI Gateway Log Viewer")

logs = read_logs()

if logs:
    st.write("### Request Logs")
    st.dataframe(logs)
else:
    st.write("No logs yet. Run some prompts through /chat first.")
