import React from 'react';

const MetricCard = ({ title, value, icon: Icon, trend, trendValue, colorClass }) => {
  return (
    <div className="card glass-panel flex-row items-center p-6 gap-6 hover:-translate-y-1 transition-transform duration-300">
      <div className={`p-4 rounded-2xl ${colorClass} bg-opacity-20`}>
        <Icon className={`w-8 h-8 ${colorClass.replace('bg-', 'text-')}`} />
      </div>
        <div className="flex flex-col flex-grow min-w-0">
          <span className="text-sm text-base-content/70 font-medium tracking-wide uppercase truncate">{title}</span>
          <div className="flex flex-wrap items-center gap-3 mt-1">
            <span className="text-3xl font-bold text-base-content">{value}</span>
            {trend && (
              <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold ${trend === 'up' ? 'bg-error/20 text-error' : 'bg-success/20 text-success'}`}>
                {trend === 'up' ? '↑' : '↓'} {trendValue}
              </span>
            )}
          </div>
        </div>
    </div>
  );
};

export default MetricCard;
