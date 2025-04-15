import streamlit as st
import os
from config.settings import UPLOAD_FOLDER
from services.ocr_service import extract_receipt_data
from services.db_service import save_receipt

def render():
    st.header("📤 Upload a Receipt")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(file_path, caption="Uploaded Receipt", use_column_width=True)

        receipt_data = extract_receipt_data(file_path)

        st.subheader("Extracted Data")
        st.json(receipt_data)

        if st.button("Save Receipt"):
            save_receipt(receipt_data, file_path)
            st.success("Receipt saved successfully!")
