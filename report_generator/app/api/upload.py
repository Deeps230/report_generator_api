from fastapi import APIRouter, File, UploadFile
import os, shutil

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{file_type}")
def upload_file(file_type: str, file: UploadFile = File(...)):
    if file_type not in ["input", "reference"]:
        return {"error": "file_type must be either 'input' or 'reference'"}
    
    file_path = os.path.join(UPLOAD_DIR, f"{file_type}.csv")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": f"{file_type}.csv uploaded successfully"}
