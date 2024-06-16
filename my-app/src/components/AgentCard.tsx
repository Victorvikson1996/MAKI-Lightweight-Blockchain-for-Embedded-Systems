import React from 'react';
import MetricsChart from './MetricsChart';
import MetricsList from './MetricList';

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

interface AgentCardProps {
  agentName: string;
  metrics: Metric[];
}

const AgentCard: React.FC<AgentCardProps> = ({ agentName, metrics }) => {
  return (
    <div className='bg-gray-800 text-white shadow-md rounded p-4'>
      <h2 className='text-2xl font-bold mb-4'>{agentName}</h2>
      <MetricsChart metrics={metrics.slice(0, 5)} />
      <MetricsList metrics={metrics.slice(0, 5)} />
    </div>
  );
};

export default AgentCard;
