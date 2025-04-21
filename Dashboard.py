from config.env import load_config
load_config()

import streamlit as st
import os
from datetime import datetime
from services.db_service import get_all_receipts
from config.settings import UPLOAD_FOLDER

st.header("📊 Dashboard")

receipts = get_all_receipts()

if not receipts:
    st.info("No receipts found yet.")
    st.stop()

# -- Utility to parse date
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%y")
    except Exception:
        return datetime.min

# -- Sorting dropdown
sort_options = {
    "Date (Newest First)": lambda r: parse_date(r.get("purchase_date", "")),
    "Date (Oldest First)": lambda r: parse_date(r.get("purchase_date", "")),
    "Store Name (A-Z)": lambda r: r.get("store_name", "").lower(),
    "Total Amount (High to Low)": lambda r: float(r.get("total_amount", 0)),
    "Total Amount (Low to High)": lambda r: float(r.get("total_amount", 0))
}

sort_choice = st.selectbox("Sort receipts by", list(sort_options.keys()))

reverse_sort = sort_choice not in ["Date (Oldest First)", "Total Amount (Low to High)"]
receipts = sorted(receipts, key=sort_options[sort_choice], reverse=reverse_sort)

# -- Display custom receipt entries
for receipt in receipts:
    with st.expander(f"🧾 {receipt.get('store_name', 'Unknown')} — {receipt.get('purchase_date', 'Unknown')}"):
        cols = st.columns([2, 3])

        # Image
        image_path = os.path.join(UPLOAD_FOLDER, receipt.get("image_name", ""))
        if os.path.exists(image_path):
            cols[0].image(image_path, caption="Receipt Image", use_column_width=True)
        else:
            cols[0].warning("Image not found")

        # Metadata
        cols[1].markdown(f"**Store:** {receipt.get('store_name', 'N/A')}")
        cols[1].markdown(f"**Date:** {receipt.get('purchase_date', 'N/A')}")
        cols[1].markdown(f"**Category:** {receipt.get('category_of_purchase', 'N/A')}")
        cols[1].markdown(f"**Subtotal:** ${receipt.get('subtotal', '0.00')}")
        cols[1].markdown(f"**Total:** ${receipt.get('total_amount', '0.00')}")
        cols[1].markdown(f"**Payment Type:** {receipt.get('payment_type', 'N/A')}")

# -- Total amount
total_spent = sum(
    float(receipt.get("total_amount", 0))
    for receipt in receipts
    if receipt.get("total_amount") is not None
)

st.markdown("---")
st.metric("💰 Total Spent", f"${total_spent:.2f}")
