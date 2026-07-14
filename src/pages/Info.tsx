import React from 'react';
import { HelpCircle, Mail, Shield } from 'lucide-react';

export default function Info() {
  return (
    <div className="grid-2">
      <div className="glass-card">
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1.5rem' }}>
          <HelpCircle color="var(--accent)" /> FAQ
        </h2>
        <div style={{ marginBottom: '1rem' }}>
          <h4 style={{ marginBottom: '0.5rem', color: '#fff' }}>How long does processing take?</h4>
          <p>Processing typically takes between 10 to 40 seconds depending on the video resolution and length.</p>
        </div>
        <div>
          <h4 style={{ marginBottom: '0.5rem', color: '#fff' }}>What formats are supported?</h4>
          <p>We currently support MP4, MOV, WEBM, and MKV video formats.</p>
        </div>
      </div>

      <div className="glass-card">
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1.5rem' }}>
          <Shield color="var(--accent)" /> Privacy Policy
        </h2>
        <p>Your privacy is our priority.</p>
        <ul style={{ color: 'var(--text-muted)', marginTop: '1rem', paddingLeft: '1.5rem', lineHeight: '1.6' }}>
          <li>All uploaded files are temporarily stored for processing.</li>
          <li>We automatically clean up original video files after the watermark is removed.</li>
          <li>Processed videos are kept strictly for your download and are not shared.</li>
        </ul>
      </div>

      <div className="glass-card" style={{ gridColumn: '1 / -1' }}>
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1.5rem' }}>
          <Mail color="var(--accent)" /> Contact Us
        </h2>
        <p>If you encounter any issues with the Vizard Watermark Remover, please reach out to our support team.</p>
        <p style={{ marginTop: '1rem', fontWeight: 'bold' }}>Email: support@vizard-watermark.example.com</p>
      </div>
    </div>
  );
}
