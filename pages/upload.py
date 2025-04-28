import streamlit as st
import os
from datetime import datetime
from config.settings import UPLOAD_FOLDER
from services.ocr_service import upload_receipt
from services.db_service import save_receipt

st.header("📤 Upload a Receipt")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Save temporarily
    temp_file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(temp_file_path, caption="Uploaded Receipt", use_container_width=True)

    # Use st.session_state to prevent multiple API calls
    if "extracted_data" not in st.session_state:
        receipt_data = upload_receipt(temp_file_path)
        st.session_state["extracted_data"] = receipt_data
    else:
        receipt_data = st.session_state["extracted_data"]

    st.subheader("📝 Edit Extracted Data Before Saving")

    # Editable fields
    store_name = st.text_input("Store Name", value=receipt_data.get("store_name", ""))
    purchase_date = st.text_input("Purchase Date (MM/DD/YY)", value=receipt_data.get("purchase_date", ""))
    category = st.text_input("Category of Purchase", value=receipt_data.get("category", ""))
    subtotal = st.text_input("Subtotal", value=receipt_data.get("subtotal", ""))
    total_amount = st.text_input("Total Amount", value=receipt_data.get("total_amount", ""))
    payment_type = st.text_input("Payment Type", value=receipt_data.get("payment_type", ""))  # optional

    if st.button("Save Receipt"):
        # Assemble corrected data
        corrected_data = {
            "store_name": store_name,
            "purchase_date": purchase_date,
            "category": category,
            "subtotal": subtotal,
            "total_amount": total_amount,
            "payment_type": payment_type,
        }

        # Create unified base filename
        safe_store_name = store_name.replace(" ", "").lower()
        try:
            date_obj = datetime.strptime(purchase_date, "%m/%d/%y")
            formatted_date = date_obj.strftime("%m%d%Y")
        except Exception:
            formatted_date = datetime.now().strftime("%m%d%Y")

        file_base_name = f"{safe_store_name}{formatted_date}"

        # New image path
        ext = os.path.splitext(uploaded_file.name)[1]
        new_image_path = os.path.join(UPLOAD_FOLDER, f"{file_base_name}{ext}")
        os.rename(temp_file_path, new_image_path)

        # Save corrected data with matching base name
        save_receipt(corrected_data, f"{file_base_name}")
        st.session_state.new_upload = True

        st.success(f"Receipt saved successfully as {file_base_name}{ext}!")
        
        # Clear session so next upload can happen clean
        del st.session_state["extracted_data"]
