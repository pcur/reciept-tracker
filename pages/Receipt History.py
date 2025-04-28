import streamlit as st
import os
import json
from datetime import datetime
from services.db_service import get_all_receipts
from config.settings import UPLOAD_FOLDER

st.header("📊 Receipt History")

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

# -- Utility to save updated receipt
def save_receipt_update(receipt, filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        with open(file_path, "w") as f:
            json.dump(receipt, f, indent=4)
    except Exception as e:
        st.error(f"Failed to save receipt: {e}")

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

# -- Setup session state for edit modes
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {}

# -- Display custom receipt entries
for idx, receipt in enumerate(receipts):
    image_name = receipt.get("image_name", "")
    expander_label = f"🧾 {receipt.get('store_name', 'Unknown')} — {receipt.get('purchase_date', 'Unknown')}"
    with st.expander(expander_label):
        cols = st.columns([2, 3])

        # Image
        image_path = os.path.join(UPLOAD_FOLDER, image_name)
        if os.path.exists(image_path):
            cols[0].image(image_path, caption="Receipt Image", use_container_width=True)
        else:
            cols[0].warning("Image not found")

        # Edit mode toggle
        if st.session_state.edit_mode.get(image_name, False):
            # Editable fields
            store_name = cols[1].text_input("Store", receipt.get("store_name", ""), key=f"store_{idx}")
            purchase_date = cols[1].text_input("Purchase Date (MM/DD/YY)", receipt.get("purchase_date", ""), key=f"date_{idx}")
            category = cols[1].text_input("Category", receipt.get("category", ""), key=f"category_{idx}")
            subtotal = cols[1].text_input("Subtotal", receipt.get("subtotal", ""), key=f"subtotal_{idx}")
            total_amount = cols[1].text_input("Total Amount", receipt.get("total_amount", ""), key=f"total_{idx}")
            payment_type = cols[1].text_input("Payment Type", receipt.get("payment_type", ""), key=f"payment_{idx}")

            if cols[1].button("Save Changes", key=f"save_{idx}"):
                # Update the receipt
                receipt["store_name"] = store_name
                receipt["purchase_date"] = purchase_date
                receipt["category_of_purchase"] = category
                receipt["subtotal"] = subtotal
                receipt["total_amount"] = total_amount
                receipt["payment_type"] = payment_type

                save_receipt_update(receipt, image_name.replace(".png", ".json").replace(".jpg", ".json").replace(".jpeg", ".json"))
                st.success("Receipt updated!")
                st.session_state.edit_mode[image_name] = False  # Turn off edit mode

            if cols[1].button("Cancel", key=f"cancel_{idx}"):
                st.session_state.edit_mode[image_name] = False  # Cancel editing

        else:
            # Read-only display
            cols[1].markdown(f"**Store:** {receipt.get('store_name', 'N/A')}")
            cols[1].markdown(f"**Date:** {receipt.get('purchase_date', 'N/A')}")
            cols[1].markdown(f"**Category:** {receipt.get('category', 'N/A')}")
            cols[1].markdown(f"**Subtotal:** ${receipt.get('subtotal', '0.00')}")
            cols[1].markdown(f"**Total:** ${receipt.get('total_amount', '0.00')}")
            cols[1].markdown(f"**Payment Type:** {receipt.get('payment_type', 'N/A')}")

            if cols[1].button("Edit", key=f"edit_{idx}"):
                st.session_state.edit_mode[image_name] = True

# -- Total amount
total_spent = sum(
    float(receipt.get("total_amount", 0))
    for receipt in receipts
    if receipt.get("total_amount") is not None
)

st.markdown("---")
st.metric("💰 Total Spent", f"${total_spent:.2f}")
