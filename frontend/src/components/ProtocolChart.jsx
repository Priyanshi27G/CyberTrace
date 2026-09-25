import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

export default function ProtocolChart() {
  const data = [
    { name: 'TCP', value: 4500, color: '#3b82f6' }, // blue-500
    { name: 'UDP', value: 3000, color: '#10b981' }, // emerald-500
    { name: 'ICMP', value: 1000, color: '#f59e0b' }, // amber-500
    { name: 'HTTP/S', value: 6500, color: '#8b5cf6' }, // violet-500
    { name: 'DNS', value: 1200, color: '#ec4899' }, // pink-500
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-base-200 border border-base-content/10 p-3 rounded-lg shadow-xl">
          <p className="font-bold text-base-content">{payload[0].name}</p>
          <p className="text-sm" style={{ color: payload[0].payload.color }}>
            {payload[0].value.toLocaleString()} packets
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card bg-base-100/50 backdrop-blur-md border border-base-content/10 shadow-xl h-full">
      <div className="card-body p-6">
        <h3 className="text-xl font-bold mb-4">Protocol Distribution</h3>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
                stroke="none"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend verticalAlign="bottom" height={36} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
