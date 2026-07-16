import os
import subprocess
import traceback
from api.database import update_job
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOVE_SCRIPT = os.path.join(BASE_DIR, "remove_watermark.py")

def process_video_task(job_id: str, input_path: str, output_path: str):
    try:
        update_job(job_id, status='processing', progress=0)
        
        # We call the existing script
        cmd = [sys.executable, REMOVE_SCRIPT, input_path, output_path]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        stdout_lines = []
        for line in process.stdout:
            stdout_lines.append(line)
            # Try to parse progress from script output if possible
            # The script outputs things like: "Pass 2/2: applying masked removal..."
            # and "  120/420 frames"
            line = line.strip()
            if "Pass 1/2" in line:
                update_job(job_id, progress=10)
            elif "Pass 2/2" in line:
                update_job(job_id, progress=50)
            elif "frames" in line and "/" in line:
                try:
                    parts = line.split()[0].split("/")
                    if len(parts) == 2:
                        current = int(parts[0])
                        total = int(parts[1])
                        progress = 50 + int((current / total) * 45)
                        update_job(job_id, progress=progress)
                except:
                    pass
            elif "Merging audio" in line:
                update_job(job_id, progress=95)
                
        process.wait()
        
        if process.returncode == 0:
            update_job(job_id, status='completed', progress=100, output_filename=os.path.basename(output_path))
        else:
            error_log = "".join(stdout_lines[-10:]).strip()
            update_job(job_id, status='failed', error_message=f"Script failed: {error_log}")
            
    except Exception as e:
        error_trace = traceback.format_exc()
        update_job(job_id, status='failed', error_message=str(e))
    finally:
        # Temporary file cleanup (Input file only, keep output for download)
        if os.path.exists(input_path):
            try:
                os.remove(input_path)
            except:
                pass
