import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import Preview from './pages/Preview';
import Processing from './pages/Processing';
import History from './pages/History';
import Info from './pages/Info';

function Navigation() {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path ? 'active' : '';

  return (
    <nav className="navbar">
      <h2><span style={{color: 'var(--accent)'}}>Vizard</span> Watermark Remover</h2>
      <div className="nav-links">
        <Link to="/" className={isActive('/')}>Upload</Link>
        <Link to="/history" className={isActive('/history')}>History</Link>
        <Link to="/info" className={isActive('/info')}>Info</Link>
        <a href="/index.html" target="_blank" rel="noreferrer">Legacy UI</a>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navigation />
        <main className="animate-fade-in">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/preview" element={<Preview />} />
            <Route path="/processing/:jobId" element={<Processing />} />
            <Route path="/history" element={<History />} />
            <Route path="/info" element={<Info />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
