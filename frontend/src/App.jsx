import React, { useState, useEffect } from 'react';
import { Activity, Shield, Users, Network, Moon, Sun, Search, Bell, Menu } from 'lucide-react';
import MetricCard from './components/MetricCard';
import AlertPanel from './components/AlertPanel';
import TopTalkersChart from './components/TopTalkersChart';

function App() {
  const [theme, setTheme] = useState('corporate');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === 'corporate' ? 'dim' : 'corporate');
  };

  return (
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
          <a href="#" className="flex items-center gap-3 px-4 py-3 bg-primary/10 text-primary rounded-xl font-medium transition-colors">
            <Activity className="w-5 h-5" />
            Dashboard
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 text-base-content/70 hover:bg-base-200 rounded-xl font-medium transition-colors">
            <Network className="w-5 h-5" />
            Network Traffic
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 text-base-content/70 hover:bg-base-200 rounded-xl font-medium transition-colors">
            <Shield className="w-5 h-5" />
            Threats
          </a>
          <a href="#" className="flex items-center gap-3 px-4 py-3 text-base-content/70 hover:bg-base-200 rounded-xl font-medium transition-colors">
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

        {/* Dashboard Content */}
        <div className="p-6 md:p-8 flex-1 overflow-auto">
          <div className="max-w-7xl mx-auto space-y-8">
            
            <div className="flex justify-between items-end">
              <div>
                <h2 className="text-3xl font-bold text-base-content">Overview</h2>
                <p className="text-base-content/60 mt-1">Real-time network security monitoring.</p>
              </div>
              <button className="btn btn-primary shadow-lg shadow-primary/30">
                Generate Report
              </button>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricCard 
                title="Total Traffic" 
                value="2.4 TB" 
                icon={Activity} 
                trend="up" 
                trendValue="12%" 
                colorClass="bg-primary text-primary"
              />
              <MetricCard 
                title="Active Threats" 
                value="14" 
                icon={Shield} 
                trend="down" 
                trendValue="3%" 
                colorClass="bg-error text-error"
              />
              <MetricCard 
                title="Connected Users" 
                value="1,284" 
                icon={Users} 
                trend="up" 
                trendValue="5%" 
                colorClass="bg-secondary text-secondary"
              />
              <MetricCard 
                title="Monitored IPs" 
                value="8,092" 
                icon={Network} 
                colorClass="bg-accent text-accent"
              />
            </div>

            {/* Charts & Alerts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 min-h-[400px]">
                <TopTalkersChart />
              </div>
              <div className="min-h-[400px]">
                <AlertPanel />
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
