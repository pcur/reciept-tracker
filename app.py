import streamlit as st

st.set_page_config(page_title="Receipt Tracker", layout="wide")

st.title("📄 Receipt Tracker")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload Receipt", "Dashboard"])

if page == "Upload Receipt":
    from pages import upload
    upload.render()
elif page == "Dashboard":
    from pages import dashboard
    dashboard.render()
