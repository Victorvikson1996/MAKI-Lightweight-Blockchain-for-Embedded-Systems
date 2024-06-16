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

interface MetricsListProps {
  metrics: Metric[];
}

const MetricsList: React.FC<MetricsListProps> = ({ metrics }) => {
  return (
    <div className='mt-4'>
      <h3 className='text-xl font-bold mb-2'>Metrics List</h3>
      <ul>
        {metrics.map((metric, index) => (
          <li key={index} className='mb-2'>
            <div className='flex items-center'>
              <div className='flex-1'>
                <p>PID: {metric.pid}</p>
                <p>Operation: {metric.operation}</p>
                <p>Details: {metric.details}</p>
                <p>CPU Usage: {metric.cpu_usage}%</p>
                <p>Memory Usage: {metric.memory_percent}%</p>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MetricsList;
