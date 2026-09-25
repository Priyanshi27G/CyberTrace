import React from 'react';
import { Shield, AlertTriangle } from 'lucide-react';

export default function Threats() {
  return (
    <div className="p-6 md:p-8 flex-1 overflow-auto flex items-center justify-center">
      <div className="text-center space-y-4">
        <div className="bg-error/20 text-error w-20 h-20 rounded-full flex items-center justify-center mx-auto">
          <AlertTriangle className="w-10 h-10" />
        </div>
        <h2 className="text-3xl font-bold text-base-content">Threat Intelligence</h2>
        <p className="text-base-content/60">Module under construction. Check back later.</p>
      </div>
    </div>
  );
}
