from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.services.transformer import generate_report
import os

router = APIRouter()

@router.post("/generate")
def trigger_report():
    generate_report()
    return {"message": "Report generated successfully."}

@router.get("/download")
def download_report():
    file_path = "reports/output.csv"
    if not os.path.exists(file_path):
        return {"error": "Report not found"}
    return FileResponse(file_path, media_type="text/csv", filename="output.csv")
