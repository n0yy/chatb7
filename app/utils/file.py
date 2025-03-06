import os

PDF_STORAGE_PATH = "../data/docs_store/"

def save_uploaded_file(upload_file) -> str: 
    """
    Saves the uploaded file to the specified directory.

    Parameters:
    upload_file: A file-like object representing the uploaded file.

    Returns:
    str: The path where the uploaded file is saved.
    """

    if not os.path.exists(PDF_STORAGE_PATH):
        os.makedirs(PDF_STORAGE_PATH)
    path = PDF_STORAGE_PATH + upload_file.name
    with open(path, "wb") as f:
        f.write(upload_file.getbuffer())
    return path