from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from app.utils.file_handler import parse_csv
from app.services.transformer import transform_data
from app.core.config import load_transformation_rules

app = FastAPI()

UPLOAD_DIR = "uploads/"
REPORT_DIR = "reports/"
CONFIG_DIR = "config/"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

@app.post("/upload/input/")
async def upload_input(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, "input.csv")
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "Input file uploaded."}

@app.post("/upload/reference/")
async def upload_reference(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, "reference.csv")
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "Reference file uploaded."}

@app.post("/config/rules/")
async def upload_rules(file: UploadFile = File(...)):
    path = os.path.join(CONFIG_DIR, "transformation_rules.yaml")
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "Rules uploaded."}

@app.post("/report/generate/")
async def generate_report():
    try:
        rules = load_transformation_rules()
        input_df = parse_csv(os.path.join(UPLOAD_DIR, "input.csv"))
        ref_df = parse_csv(os.path.join(UPLOAD_DIR, "reference.csv"))

        output_df = transform_data(input_df, ref_df, rules)
        output_path = os.path.join(REPORT_DIR, "output.csv")
        output_df.to_csv(output_path, index=False)

        return {"message": "Report generated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report/download/")
async def download_report():
    path = os.path.join(REPORT_DIR, "output.csv")
    if os.path.exists(path):
        return FileResponse(path, filename="output.csv", media_type="text/csv")
    raise HTTPException(status_code=404, detail="Report not found.")
