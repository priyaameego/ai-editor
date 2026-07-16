import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, Download, CheckCircle, XCircle } from 'lucide-react';
import axios from 'axios';

export default function Processing() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) return;
    
    const interval = setInterval(async () => {
      try {
        const apiBase = import.meta.env.VITE_API_URL || 'https://ai-editor-10.onrender.com';
        const res = await axios.get(`${apiBase}/api/status/${jobId}`);
        setJob(res.data);
        
        if (res.data.status === 'completed' || res.data.status === 'failed') {
          clearInterval(interval);
        }
      } catch (err: any) {
        console.error(err);
        const errMsg = err.response?.data?.detail || "Failed to fetch status from backend server. Backend might be unreachable.";
        setError(errMsg);
        clearInterval(interval);
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, [jobId]);

  if (error) {
    return (
      <div className="glass-card" style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'center' }}>
        <XCircle size={48} color="var(--danger)" style={{ marginBottom: '1rem' }} />
        <h2>Error</h2>
        <p>{error}</p>
        <button className="btn btn-secondary" style={{ marginTop: '2rem' }} onClick={() => navigate('/')}>
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="glass-card" style={{ maxWidth: '600px', margin: '0 auto', textAlign: 'center' }}>
      {!job || job.status === 'queued' || job.status === 'processing' ? (
        <>
          <Loader2 size={48} color="var(--accent)" style={{ margin: '0 auto 1.5rem', animation: 'spin 2s linear infinite' }} />
          <h2>Processing Video</h2>
          <p style={{ marginBottom: '2rem' }}>Please wait while we remove the watermark...</p>
          
          <div className="progress-container">
            <div className="progress-bar-bg">
              <div className="progress-bar-fill" style={{ width: `${job?.progress || 0}%` }}></div>
            </div>
            <p style={{ marginTop: '10px', color: 'var(--text-muted)' }}>{job?.progress || 0}% Complete</p>
          </div>
        </>
      ) : job.status === 'completed' ? (
        <>
          <CheckCircle size={48} color="var(--success)" style={{ marginBottom: '1.5rem' }} />
          <h2>Processing Complete!</h2>
          <p style={{ marginBottom: '2rem' }}>Your video is ready to download.</p>
          <a href={`${import.meta.env.VITE_API_URL || 'https://ai-editor-10.onrender.com'}/api/download/${job.job_id}`} className="btn btn-primary" download>
            <Download size={18} /> Download Clean Video
          </a>
          <button className="btn btn-secondary" style={{ marginTop: '1rem', marginLeft: '1rem' }} onClick={() => navigate('/')}>
            Process Another
          </button>
        </>
      ) : (
        <>
          <XCircle size={48} color="var(--danger)" style={{ marginBottom: '1.5rem' }} />
          <h2>Processing Failed</h2>
          <p style={{ marginBottom: '2rem' }}>{job.error_message || "An unknown error occurred."}</p>
          <button className="btn btn-secondary" onClick={() => navigate('/')}>
            Try Again
          </button>
        </>
      )}
      <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
