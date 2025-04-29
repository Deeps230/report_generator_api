from fastapi import APIRouter, File, UploadFile
import os, shutil

router = APIRouter()
CONFIG_DIR = "config"
os.makedirs(CONFIG_DIR, exist_ok=True)

@router.post("/rules")
def upload_rules(file: UploadFile = File(...)):
    file_path = os.path.join(CONFIG_DIR, "transformation_rules.yaml")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "Transformation rules uploaded successfully"}
