import sqlite3
import os
import json
import uuid
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'jobs.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            filename TEXT NOT NULL,
            output_filename TEXT,
            created_at TEXT NOT NULL,
            completed_at TEXT,
            progress INTEGER DEFAULT 0,
            error_message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_job(filename: str) -> str:
    job_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO jobs (job_id, status, filename, created_at)
        VALUES (?, ?, ?, ?)
    ''', (job_id, 'queued', filename, created_at))
    conn.commit()
    conn.close()
    return job_id

def get_job(job_id: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE job_id = ?', (job_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_job(job_id: str, status: str = None, progress: int = None, output_filename: str = None, error_message: str = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if status is not None:
        updates.append("status = ?")
        params.append(status)
        if status in ['completed', 'failed']:
            updates.append("completed_at = ?")
            params.append(datetime.utcnow().isoformat())
    if progress is not None:
        updates.append("progress = ?")
        params.append(progress)
    if output_filename is not None:
        updates.append("output_filename = ?")
        params.append(output_filename)
    if error_message is not None:
        updates.append("error_message = ?")
        params.append(error_message)
        
    if updates:
        params.append(job_id)
        cursor.execute(f'''
            UPDATE jobs 
            SET {", ".join(updates)}
            WHERE job_id = ?
        ''', tuple(params))
        conn.commit()
        
    conn.close()

def get_all_jobs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
