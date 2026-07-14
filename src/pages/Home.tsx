import React, { useState, useCallback } from 'react';
import { Upload, X, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function Home() {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") setDragActive(true);
    else if (e.type === "dragleave") setDragActive(false);
  }, []);

  const validateFile = (f: File) => {
    if (!f.type.startsWith('video/') && !f.name.match(/\.(mp4|mov|webm|mkv)$/i)) {
      setError("Please upload a valid video file.");
      return false;
    }
    setError(null);
    return true;
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      if (validateFile(e.dataTransfer.files[0])) {
        setFile(e.dataTransfer.files[0]);
      }
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      if (validateFile(e.target.files[0])) {
        setFile(e.target.files[0]);
      }
    }
  };

  const startUpload = async () => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      // In Docker Compose, the Vite proxy or absolute URL needs to be set.
      // We will assume Vite is proxying /api to the backend.
      const response = await axios.post('/api/upload', formData, {
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 100));
          setProgress(percentCompleted);
        }
      });
      navigate(`/processing/${response.data.job_id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Upload failed. Please try again.");
      setUploading(false);
    }
  };

  return (
    <div className="glass-card" style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'center' }}>
      <h1>Upload Video</h1>
      <p style={{ marginBottom: '2rem' }}>Securely upload your video to start removing the watermark.</p>
      
      {!file ? (
        <div 
          className={`dropzone ${dragActive ? 'active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-upload')?.click()}
        >
          <Upload className="dropzone-icon" />
          <p>Drag and drop your video here<br/>or click to browse</p>
          <input 
            id="file-upload" 
            type="file" 
            accept="video/*,.mp4,.mov,.webm" 
            style={{ display: 'none' }} 
            onChange={handleChange} 
          />
        </div>
      ) : (
        <div style={{ padding: '2rem 0' }}>
          <h3 style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
            {file.name}
            {!uploading && (
              <X 
                style={{ cursor: 'pointer', color: 'var(--danger)' }} 
                onClick={() => setFile(null)} 
              />
            )}
          </h3>
          
          {uploading ? (
            <div className="progress-container">
              <div className="progress-bar-bg">
                <div className="progress-bar-fill" style={{ width: `${progress}%` }}></div>
              </div>
              <p style={{ marginTop: '10px', color: 'var(--accent)' }}>Uploading... {progress}%</p>
            </div>
          ) : (
            <button className="btn btn-primary" style={{ marginTop: '1rem' }} onClick={startUpload}>
              Start Processing
            </button>
          )}
        </div>
      )}

      {error && (
        <div className="toast error" style={{ position: 'relative', marginTop: '20px', bottom: 0, right: 0 }}>
          <AlertCircle size={20} />
          {error}
        </div>
      )}
    </div>
  );
}
