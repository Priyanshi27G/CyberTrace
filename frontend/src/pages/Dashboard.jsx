import React from 'react';
import { Activity, Shield, Users, Network } from 'lucide-react';
import MetricCard from '../components/MetricCard';
import AlertPanel from '../components/AlertPanel';
import TopTalkersChart from '../components/TopTalkersChart';

export default function Dashboard() {
  return (
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
  );
}
