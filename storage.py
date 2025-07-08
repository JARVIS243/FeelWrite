# storage.py

import os

# Define the upload folder for images and exported files
UPLOAD_FOLDER = "assets/uploads"

# Make sure upload directory exists
def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

# Save uploaded file and return the saved path
def save_uploaded_file(file, filename):
    ensure_upload_folder()
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path

# Return full file path for exported files (txt/pdf)
def get_export_path(username, entry_date, filetype="txt"):
    ensure_upload_folder()
    safe_name = f"{username}_{entry_date}.{filetype}"
    return os.path.join(UPLOAD_FOLDER, safe_name)
