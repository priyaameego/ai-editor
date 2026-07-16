from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import shutil

from api.database import init_db, create_job, get_job, get_all_jobs
from api.worker import process_video_task

app = FastAPI(title="Watermark Remover API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/api/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.mp4', '.mov', '.webm', '.mkv')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only video files are allowed.")
    
    # Secure validation
    input_path = os.path.join(UPLOADS_DIR, file.filename)
    
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    job_id = create_job(file.filename)
    
    output_filename = f"clean_{job_id}.mp4"
    output_path = os.path.join(OUTPUTS_DIR, output_filename)
    
    background_tasks.add_task(process_video_task, job_id, input_path, output_path)
    
    return {"job_id": job_id, "message": "Upload successful, processing started."}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/api/history")
async def get_history():
    jobs = get_all_jobs()
    return {"jobs": jobs}

@app.get("/api/download/{job_id}")
async def download_video(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Video is not ready yet")
        
    output_path = os.path.join(OUTPUTS_DIR, job['output_filename'])
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="File not found on server")
        
    return FileResponse(output_path, media_type="video/mp4", filename=job['output_filename'])
