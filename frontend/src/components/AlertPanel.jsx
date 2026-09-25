import React from 'react';
import { AlertTriangle, ShieldAlert, Info } from 'lucide-react';

const mockAlerts = [
  { id: 1, type: 'critical', title: 'DDoS Attempt Detected', time: '2 mins ago', source: '192.168.1.105' },
  { id: 2, type: 'warning', title: 'Unusual Port Scan', time: '15 mins ago', source: '10.0.0.52' },
  { id: 3, type: 'info', title: 'New Device Connected', time: '1 hour ago', source: '192.168.1.200' },
  { id: 4, type: 'warning', title: 'High Bandwidth Usage', time: '3 hours ago', source: '10.0.0.12' },
];

const getAlertConfig = (type) => {
  switch (type) {
    case 'critical':
      return { icon: ShieldAlert, color: 'text-error', bg: 'bg-error/10', border: 'border-error/20' };
    case 'warning':
      return { icon: AlertTriangle, color: 'text-warning', bg: 'bg-warning/10', border: 'border-warning/20' };
    case 'info':
    default:
      return { icon: Info, color: 'text-info', bg: 'bg-info/10', border: 'border-info/20' };
  }
};

const AlertPanel = () => {
  return (
    <div className="card glass-panel w-full h-full flex flex-col">
      <div className="card-body p-6">
        <h2 className="card-title text-xl font-bold mb-4">Recent Alerts</h2>
        <div className="flex flex-col gap-3 overflow-y-auto">
          {mockAlerts.map((alert) => {
            const config = getAlertConfig(alert.type);
            const Icon = config.icon;
            
            return (
              <div 
                key={alert.id} 
                className={`flex items-start gap-4 p-4 rounded-xl border ${config.border} ${config.bg} hover:brightness-105 transition-all`}
              >
                <div className={`mt-1 ${config.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-center mb-1">
                    <h3 className="font-semibold text-base-content">{alert.title}</h3>
                    <span className="text-xs text-base-content/60">{alert.time}</span>
                  </div>
                  <p className="text-sm text-base-content/70 font-mono">{alert.source}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default AlertPanel;
