from config.env import load_config
load_config()

import streamlit as st
from services.db_service import get_all_receipts
import pandas as pd

st.header("📊 Dashboard")

receipts = get_all_receipts()

if not receipts:
    st.info("No receipts found yet.")


df = pd.DataFrame(receipts)
st.dataframe(df)

total_spent = sum(receipt["total"] for receipt in receipts)
st.metric("Total Spent", f"${total_spent:.2f}")
