import React from 'react';
import { Network, Activity, Filter, RefreshCw, Zap } from 'lucide-react';

export default function NetworkTraffic() {
  return (
    <div className="p-6 md:p-8 flex-1 overflow-auto">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-3xl font-bold text-base-content">Network Traffic</h2>
            <p className="text-base-content/60 mt-1">Live monitoring of packet logs and connections.</p>
          </div>
          <div className="flex gap-3">
            <button className="btn btn-outline gap-2 border-base-content/20 hover:bg-base-200">
              <Filter className="w-4 h-4" />
              Filter
            </button>
            <button className="btn btn-primary shadow-lg shadow-primary/30 gap-2">
              <RefreshCw className="w-4 h-4" />
              Live Stream
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="card bg-base-100/50 backdrop-blur-md border border-base-content/10 p-6 flex flex-row items-center gap-4">
            <div className="bg-success/20 text-success p-3 rounded-xl">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-base-content/60 font-medium">Current Throughput</p>
              <h4 className="text-2xl font-bold">1.2 Gbps</h4>
            </div>
          </div>
          <div className="card bg-base-100/50 backdrop-blur-md border border-base-content/10 p-6 flex flex-row items-center gap-4">
            <div className="bg-info/20 text-info p-3 rounded-xl">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-base-content/60 font-medium">Packets/sec</p>
              <h4 className="text-2xl font-bold">45,210</h4>
            </div>
          </div>
          <div className="card bg-base-100/50 backdrop-blur-md border border-base-content/10 p-6 flex flex-row items-center gap-4">
            <div className="bg-warning/20 text-warning p-3 rounded-xl">
              <Network className="w-6 h-6" />
            </div>
            <div>
              <p className="text-sm text-base-content/60 font-medium">Active Connections</p>
              <h4 className="text-2xl font-bold">8,932</h4>
            </div>
          </div>
        </div>

        {/* Live Packet Logs Placeholder */}
        <div className="card bg-base-100/50 backdrop-blur-md border border-base-content/10 shadow-xl font-mono text-sm">
          <div className="card-body p-0">
            <div className="bg-base-200/50 p-4 border-b border-base-content/10 flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-error animate-pulse"></div>
              <span className="font-semibold uppercase tracking-wider text-xs">Live Capture Feed</span>
            </div>
            <div className="p-4 space-y-2 max-h-[500px] overflow-y-auto">
              {[...Array(15)].map((_, i) => (
                <div key={i} className="flex gap-4 items-center p-2 hover:bg-base-200/50 rounded transition-colors">
                  <span className="text-base-content/40 w-24">14:02:{59 - i}.{Math.floor(Math.random() * 999).toString().padStart(3, '0')}</span>
                  <span className="text-info w-32">192.168.1.{Math.floor(Math.random() * 255)}</span>
                  <span className="text-base-content/40 w-8">→</span>
                  <span className="text-warning w-32">10.0.{Math.floor(Math.random() * 255)}.{Math.floor(Math.random() * 255)}</span>
                  <span className="text-success w-16">TCP</span>
                  <span className="truncate text-base-content/60 flex-1">
                    [SYN] Seq={Math.floor(Math.random() * 10000)} Win=64240 Len=0 MSS=1460 SACK_PERM=1 TSval={Math.floor(Math.random() * 1000000)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
