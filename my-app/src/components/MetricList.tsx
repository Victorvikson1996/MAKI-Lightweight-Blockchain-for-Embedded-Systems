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
      <h3 className='text-xl font-bold mb-4 text-gray-300'>Metrics List</h3>
      <ul className='space-y-4'>
        {metrics.map((metric, index) => (
          <li key={index} className='p-4 bg-gray-900 rounded-lg shadow-md'>
            <div className='flex items-center'>
              <div className='flex-1'>
                <p className='text-sm font-semibold text-gray-400'>
                  <span className='text-gray-500'>PID:</span> {metric.pid}
                </p>
                <p className='text-sm font-semibold text-gray-400'>
                  <span className='text-gray-500'>Operation:</span>{' '}
                  {metric.operation}
                </p>
                <p className='text-sm font-semibold text-gray-400'>
                  <span className='text-gray-500'>Details:</span>{' '}
                  {metric.details}
                </p>
                <p className='text-sm font-semibold text-gray-400'>
                  <span className='text-gray-500'>CPU Usage:</span>{' '}
                  {metric.cpu_usage}%
                </p>
                <p className='text-sm font-semibold text-gray-400'>
                  <span className='text-gray-500'>Memory Usage:</span>{' '}
                  {metric.memory_percent}%
                </p>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MetricsList;
