import streamlit as st
from services.db_service import get_all_receipts
import pandas as pd

def render():
    st.header("📊 Dashboard")

    receipts = get_all_receipts()

    if not receipts:
        st.info("No receipts found yet.")
        return

    df = pd.DataFrame(receipts)
    st.dataframe(df)

    total_spent = sum(receipt["total"] for receipt in receipts)
    st.metric("Total Spent", f"${total_spent:.2f}")
