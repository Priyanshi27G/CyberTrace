import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { Activity, Shield, Users, Network, Moon, Sun, Search, Bell, Menu, FileSearch } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import NetworkTraffic from './pages/NetworkTraffic';
import PcapForensics from './pages/PcapForensics';
import Threats from './pages/Threats';
function App() {
  const [theme, setTheme] = useState('corporate');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === 'corporate' ? 'dim' : 'corporate');
  };

  return (
    <BrowserRouter>
    <div className="min-h-screen bg-base-200 flex flex-col md:flex-row transition-colors duration-300">
      {/* Sidebar */}
      <aside className="w-full md:w-64 bg-base-100 border-r border-base-content/10 hidden md:flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <div className="bg-primary text-primary-content p-2 rounded-lg">
            <Shield className="w-6 h-6" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">CyberTrace</h1>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-2">
          <NavLink to="/" className={({isActive}) => `flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-colors ${isActive ? 'bg-primary/10 text-primary' : 'text-base-content/70 hover:bg-base-200'}`}>
            <Activity className="w-5 h-5" />
            Dashboard
          </NavLink>
          <NavLink to="/network" className={({isActive}) => `flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-colors ${isActive ? 'bg-primary/10 text-primary' : 'text-base-content/70 hover:bg-base-200'}`}>
            <Network className="w-5 h-5" />
            Network Traffic
          </NavLink>
          <NavLink to="/pcap" className={({isActive}) => `flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-colors ${isActive ? 'bg-primary/10 text-primary' : 'text-base-content/70 hover:bg-base-200'}`}>
            <FileSearch className="w-5 h-5" />
            PCAP Forensics
          </NavLink>
          <NavLink to="/threats" className={({isActive}) => `flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-colors ${isActive ? 'bg-primary/10 text-primary' : 'text-base-content/70 hover:bg-base-200'}`}>
            <Shield className="w-5 h-5" />
            Threats
          </NavLink>
          <a 
            href="#" 
            className="flex items-center gap-3 px-4 py-3 text-base-content/70 hover:bg-base-200 rounded-xl font-medium transition-colors"
            onClick={(e) => {
              e.preventDefault();
              alert("Users management module is currently under construction. Please check back later.");
            }}
          >
            <Users className="w-5 h-5" />
            Users
          </a>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Navbar */}
        <header className="h-20 bg-base-100/50 backdrop-blur-md border-b border-base-content/10 flex items-center justify-between px-6 sticky top-0 z-10">
          <div className="flex items-center gap-4">
            <button className="md:hidden btn btn-ghost btn-circle">
              <Menu className="w-5 h-5" />
            </button>
            <div className="relative hidden sm:block">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-base-content/50" />
              <input 
                type="text" 
                placeholder="Search IPs, alerts..." 
                className="input input-sm input-bordered pl-9 w-64 bg-base-200/50 focus:bg-base-100 transition-colors"
              />
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <button className="btn btn-ghost btn-circle" onClick={toggleTheme}>
              {theme === 'corporate' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
            </button>
            <button className="btn btn-ghost btn-circle">
              <div className="indicator">
                <Bell className="w-5 h-5" />
                <span className="indicator-item badge badge-error badge-xs"></span>
              </div>
            </button>
            <div className="avatar placeholder ml-2">
              <div className="bg-neutral text-neutral-content rounded-full w-10">
                <span>AD</span>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/network" element={<NetworkTraffic />} />
          <Route path="/pcap" element={<PcapForensics />} />
          <Route path="/threats" element={<Threats />} />
        </Routes>
      </main>
    </div>
    </BrowserRouter>
  );
}

export default App;
