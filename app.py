import os
import tempfile
import streamlit as st
import json
from logic import process_all_pdfs

st.title("PDF Outline Extractor")

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    with tempfile.TemporaryDirectory() as temp_dir:
        input_folder = os.path.join(temp_dir, "pdfs")
        output_folder = os.path.join(temp_dir, "outputs")
        os.makedirs(input_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)

        for file in uploaded_files:
            with open(os.path.join(input_folder, file.name), "wb") as f:
                f.write(file.read())

        st.success("Files uploaded. Processing...")

        process_all_pdfs(input_folder, output_folder)

        st.subheader("Extracted Outputs")
        for file in os.listdir(output_folder):
            with open(os.path.join(output_folder, file), "r", encoding="utf-8") as f:
                st.json(json.load(f))
