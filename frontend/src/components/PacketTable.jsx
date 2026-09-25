import React from 'react';
import { Activity, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function PacketTable() {
  const dummyPackets = [
    { id: 1, time: '14:32:01', src: '192.168.1.105', dst: '8.8.8.8', proto: 'DNS', len: 74, status: 'normal' },
    { id: 2, time: '14:32:02', src: '10.0.0.5', dst: '192.168.1.100', proto: 'TCP', len: 1514, status: 'normal' },
    { id: 3, time: '14:32:03', src: '45.33.32.156', dst: '192.168.1.1', proto: 'TCP', len: 60, status: 'alert' },
    { id: 4, time: '14:32:05', src: '192.168.1.50', dst: '1.1.1.1', proto: 'UDP', len: 90, status: 'normal' },
    { id: 5, time: '14:32:08', src: '185.15.22.4', dst: '192.168.1.100', proto: 'ICMP', len: 98, status: 'warning' },
  ];

  return (
    <div className="card bg-base-100/50 backdrop-blur-md border border-base-content/10 shadow-xl overflow-hidden h-full">
      <div className="card-body p-0">
        <div className="p-6 pb-2 border-b border-base-content/10 flex justify-between items-center">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <Activity className="w-5 h-5 text-primary" />
            Live Packet Feed
          </h3>
          <span className="badge badge-success badge-sm gap-1">
            <span className="w-2 h-2 rounded-full bg-success-content animate-pulse"></span>
            Capturing
          </span>
        </div>
        
        <div className="overflow-x-auto">
          <table className="table table-zebra table-sm w-full">
            <thead>
              <tr className="bg-base-200/50">
                <th>Time</th>
                <th>Source</th>
                <th>Destination</th>
                <th>Protocol</th>
                <th>Length</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {dummyPackets.map((pkt) => (
                <tr key={pkt.id} className="hover">
                  <td className="font-mono text-xs opacity-70">{pkt.time}</td>
                  <td className="font-mono text-xs">{pkt.src}</td>
                  <td className="font-mono text-xs">{pkt.dst}</td>
                  <td>
                    <span className="badge badge-outline badge-sm font-mono opacity-80">
                      {pkt.proto}
                    </span>
                  </td>
                  <td className="font-mono text-xs opacity-70">{pkt.len}</td>
                  <td>
                    {pkt.status === 'normal' && <CheckCircle2 className="w-4 h-4 text-success" />}
                    {pkt.status === 'warning' && <ShieldAlert className="w-4 h-4 text-warning" />}
                    {pkt.status === 'alert' && <ShieldAlert className="w-4 h-4 text-error animate-pulse" />}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="p-4 bg-base-200/30 text-center border-t border-base-content/10">
          <button className="btn btn-ghost btn-sm text-primary">View Full Log</button>
        </div>
      </div>
    </div>
  );
}
