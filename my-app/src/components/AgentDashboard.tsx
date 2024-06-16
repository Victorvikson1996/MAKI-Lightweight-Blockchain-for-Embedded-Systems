import React from 'react';
import { useQuery } from 'react-query';
import AgentCard from './AgentCard';

const fetchMetrics = async (agent: string) => {
  const response = await fetch(`/data/metrics_${agent}.json`);
  if (!response.ok) {
    console.error(`Error fetching metrics for ${agent}:`, response.statusText);
    throw new Error('Network response was not ok');
  }
  return response.json();
};

const AgentsDashboard: React.FC = () => {
  const {
    data: agentAData,
    error: agentAError,
    isLoading: agentALoading
  } = useQuery('agentA', () => fetchMetrics('agent_a'));
  const {
    data: agentBData,
    error: agentBError,
    isLoading: agentBLoading
  } = useQuery('agentB', () => fetchMetrics('agent_b'));

  if (agentALoading || agentBLoading) {
    return <div className='text-white'>Loading...</div>;
  }

  if (agentAError || agentBError) {
    return <div className='text-white'>Error loading data</div>;
  }

  return (
    <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
      {agentAData && (
        <AgentCard agentName='Agent A' metrics={agentAData.slice(0, 5)} />
      )}
      {agentBData && (
        <AgentCard agentName='Agent B' metrics={agentBData.slice(0, 5)} />
      )}
    </div>
  );
};

export default AgentsDashboard;
