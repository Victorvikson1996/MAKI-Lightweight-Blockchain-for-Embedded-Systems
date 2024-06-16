import React from 'react';

interface Metric {
  operation: string;
  details: string;
  cpu_usage: number;
  memory_used: number;
  memory_total: number;
  memory_percent: number;
  data_size: number;
  num_transactions: number;
  timestamp: number;
  pid: number;
}

interface ProgressIndicatorProps {
  metrics: Metric[];
}

const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ metrics }) => {
  const latestMetric = metrics[metrics.length - 1];

  return (
    <div className='mt-4'>
      <h3 className='text-xl font-bold'>Latest Operation</h3>
      <div className='flex items-center'>
        <div className='flex-1'>
          <p>Operation: {latestMetric.operation}</p>
          <p>Details: {latestMetric.details}</p>
          <p>CPU Usage: {latestMetric.cpu_usage}%</p>
          <p>Memory Usage: {latestMetric.memory_percent}%</p>
        </div>
        <div className='w-24 h-24'>
          {/* Placeholder for agent icon */}
          <img src='/path/to/agent-icon.png' alt='Agent Icon' />
        </div>
      </div>
    </div>
  );
};

export default ProgressIndicator;
