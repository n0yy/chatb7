import os

PDF_STORAGE_PATH = "../data/docs_store/pdfs/"

def save_uploaded_file(upload_file) -> str: 
    if not os.path.exists(PDF_STORAGE_PATH):
        os.makedirs(PDF_STORAGE_PATH)
    path = PDF_STORAGE_PATH + upload_file.name
    with open(path, "wb") as f:
        f.write(upload_file.getbuffer())
    return path