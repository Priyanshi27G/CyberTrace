import React, { useState } from 'react';
import { UploadCloud, Search, FileText } from 'lucide-react';

export default function PcapForensics() {
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div className="p-6 md:p-8 flex-1 overflow-auto">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-3xl font-bold text-base-content">PCAP Forensics</h2>
            <p className="text-base-content/60 mt-1">Upload and analyze packet captures for detailed forensic investigation.</p>
          </div>
        </div>

        {/* Upload Section */}
        <div 
          className={`border-2 border-dashed rounded-3xl p-12 text-center transition-colors duration-300 ${isDragging ? 'border-primary bg-primary/10' : 'border-base-content/20 bg-base-100/50 hover:bg-base-100'}`}
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(e) => { e.preventDefault(); setIsDragging(false); }}
        >
          <div className="bg-primary/20 text-primary w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
            <UploadCloud className="w-10 h-10" />
          </div>
          <h3 className="text-2xl font-bold mb-2">Drag & Drop PCAP Files</h3>
          <p className="text-base-content/60 mb-6">Support for .pcap, .pcapng files up to 500MB</p>
          <button className="btn btn-primary px-8 rounded-full shadow-lg shadow-primary/30">
            Browse Files
          </button>
        </div>

        {/* Analysis Results Placeholder */}
        <div className="card bg-base-100/50 backdrop-blur-md border border-base-content/10 shadow-xl">
          <div className="card-body">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold flex items-center gap-2">
                <Search className="w-5 h-5 text-secondary" />
                Recent Analysis
              </h3>
              <button className="btn btn-sm btn-ghost">View All</button>
            </div>
            
            <div className="overflow-x-auto">
              <table className="table">
                <thead>
                  <tr className="border-base-content/10">
                    <th>File Name</th>
                    <th>Size</th>
                    <th>Date Analyzed</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="hover border-base-content/10 transition-colors">
                    <td className="flex items-center gap-3">
                      <div className="bg-accent/20 p-2 rounded-lg text-accent">
                        <FileText className="w-5 h-5" />
                      </div>
                      <span className="font-medium">suspicious_traffic_01.pcap</span>
                    </td>
                    <td className="text-base-content/70">45.2 MB</td>
                    <td className="text-base-content/70">Oct 24, 2023</td>
                    <td>
                      <div className="badge badge-success gap-1 p-3">
                        Analyzed
                      </div>
                    </td>
                    <td>
                      <button className="btn btn-sm btn-outline">Report</button>
                    </td>
                  </tr>
                  <tr className="hover border-base-content/10 transition-colors">
                    <td className="flex items-center gap-3">
                      <div className="bg-accent/20 p-2 rounded-lg text-accent">
                        <FileText className="w-5 h-5" />
                      </div>
                      <span className="font-medium">malware_sample_capture.pcap</span>
                    </td>
                    <td className="text-base-content/70">128.5 MB</td>
                    <td className="text-base-content/70">Oct 22, 2023</td>
                    <td>
                      <div className="badge badge-warning gap-1 p-3">
                        Pending
                      </div>
                    </td>
                    <td>
                      <button className="btn btn-sm btn-outline" disabled>Report</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
