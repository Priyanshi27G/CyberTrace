import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { ip: '192.168.1.10', traffic: 4000 },
  { ip: '10.0.0.5', traffic: 3000 },
  { ip: '172.16.0.4', traffic: 2000 },
  { ip: '192.168.1.55', traffic: 2780 },
  { ip: '10.0.0.21', traffic: 1890 },
  { ip: '192.168.1.100', traffic: 2390 },
  { ip: '172.16.0.8', traffic: 3490 },
];

const TopTalkersChart = () => {
  return (
    <div className="card glass-panel w-full h-full">
      <div className="card-body p-6">
        <h2 className="card-title text-xl font-bold mb-6">Top Talkers (MB)</h2>
        <div className="w-full h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="currentColor" className="opacity-10" />
              <XAxis 
                dataKey="ip" 
                tick={{fill: 'currentColor', opacity: 0.7, fontSize: 12}}
                axisLine={{stroke: 'currentColor', opacity: 0.2}}
                tickLine={false}
              />
              <YAxis 
                tick={{fill: 'currentColor', opacity: 0.7, fontSize: 12}}
                axisLine={{stroke: 'currentColor', opacity: 0.2}}
                tickLine={false}
              />
              <Tooltip 
                cursor={{fill: 'currentColor', opacity: 0.05}}
                contentStyle={{
                  backgroundColor: 'hsl(var(--b1))',
                  border: '1px solid hsl(var(--bc) / 0.1)',
                  borderRadius: '0.75rem',
                  color: 'hsl(var(--bc))'
                }}
              />
              <Bar 
                dataKey="traffic" 
                fill="#10B981" 
                radius={[4, 4, 0, 0]} 
                animationDuration={1500}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default TopTalkersChart;
