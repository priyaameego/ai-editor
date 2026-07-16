import { useEffect, useState } from 'react';
import axios from 'axios';
import { Clock, CheckCircle, XCircle, Loader2, Download, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function History() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const apiBase = import.meta.env.VITE_API_URL || 'https://ai-editor-10.onrender.com';
        const res = await axios.get(`${apiBase}/api/history`);
        setJobs(res.data.jobs);
        setError(null);
      } catch (err: any) {
        console.error(err);
        setError("Failed to fetch processing history from backend server. Backend might be unreachable.");
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const getStatusIcon = (status: string) => {
    switch(status) {
      case 'completed': return <CheckCircle size={20} color="var(--success)" />;
      case 'failed': return <XCircle size={20} color="var(--danger)" />;
      case 'processing': return <Loader2 size={20} color="var(--accent)" style={{ animation: 'spin 2s linear infinite' }} />;
      default: return <Clock size={20} color="var(--text-muted)" />;
    }
  };

  return (
    <div className="glass-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Clock /> Processing History
      </h2>
      
      {error && (
        <div className="toast error" style={{ position: 'relative', marginTop: '10px', marginBottom: '20px', bottom: 0, right: 0 }}>
          <AlertCircle size={20} />
          {error}
        </div>
      )}

      {loading ? (
        <p style={{ textAlign: 'center', padding: '2rem' }}>Loading history...</p>
      ) : jobs.length === 0 ? (
        <p style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>No previous jobs found.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {jobs.map(job => (
            <div key={job.job_id} style={{
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between',
              padding: '1rem',
              background: 'rgba(255,255,255,0.02)',
              borderRadius: '8px',
              border: '1px solid var(--panel-border)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                {getStatusIcon(job.status)}
                <div>
                  <h4 style={{ margin: 0 }}>{job.filename}</h4>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    {new Date(job.created_at).toLocaleString()} - {job.status.toUpperCase()}
                  </span>
                </div>
              </div>
              
              <div>
                {job.status === 'completed' && (
                  <a href={`${import.meta.env.VITE_API_URL || 'https://ai-editor-10.onrender.com'}/api/download/${job.job_id}`} className="btn btn-primary" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }} download>
                    <Download size={16} /> Download
                  </a>
                )}
                {(job.status === 'processing' || job.status === 'queued') && (
                  <Link to={`/processing/${job.job_id}`} className="btn btn-secondary" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>
                    View Status
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
      <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
