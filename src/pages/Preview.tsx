import React, { useState } from 'react';
import { Settings, Sliders } from 'lucide-react';

export default function Preview() {
  const [sliderPos, setSliderPos] = useState(50);

  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSliderPos(Number(e.target.value));
  };

  return (
    <div className="grid-2" style={{ alignItems: 'start' }}>
      <div className="glass-card">
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1.5rem' }}>
          <Sliders color="var(--accent)" /> Compare Preview
        </h2>
        
        {/* Placeholder Before/After Comparison */}
        <div style={{ position: 'relative', width: '100%', height: '400px', backgroundColor: '#000', borderRadius: '8px', overflow: 'hidden' }}>
          <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff' }}>
            Before
          </div>
          <div style={{ position: 'absolute', top: 0, left: 0, width: `${sliderPos}%`, height: '100%', backgroundColor: '#222', borderRight: '2px solid #fff', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', overflow: 'hidden' }}>
            <div style={{ width: '100%', minWidth: '300px', textAlign: 'center' }}>After</div>
          </div>
          <input 
            type="range" 
            min="0" max="100" 
            value={sliderPos} 
            onChange={handleSliderChange}
            style={{ position: 'absolute', bottom: '20px', left: '10%', width: '80%', zIndex: 10 }}
          />
        </div>
        <p style={{ textAlign: 'center', marginTop: '1rem', color: 'var(--text-muted)' }}>
          Note: This is a visual representation. Full processing happens on the backend.
        </p>
      </div>

      <div className="glass-card">
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '1.5rem' }}>
          <Settings color="var(--accent)" /> Settings Panel
        </h2>
        
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Processing Method</label>
          <select>
            <option>Masked temporal min (Default)</option>
            <option>Reverse alpha blend</option>
            <option>Edge fill inpaint</option>
          </select>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Feather Edges</label>
          <input type="range" min="0" max="20" defaultValue="10" />
        </div>
        
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Bright Threshold</label>
          <input type="range" min="120" max="220" defaultValue="165" />
        </div>

        <button className="btn btn-primary" style={{ width: '100%' }}>
          Save Settings
        </button>
      </div>
    </div>
  );
}
