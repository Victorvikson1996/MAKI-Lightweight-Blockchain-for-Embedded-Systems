import React from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import AgentsDashboard from './components/AgentDashboard';

const queryClient = new QueryClient();

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <div
        className='container mx-auto p-4'
        style={{ backgroundColor: '#1e2738' }}
      >
        <h1 className='text-3xl font-bold mb-4 text-white'>
          Agent Metrics Dashboard
        </h1>
        <AgentsDashboard />
      </div>
    </QueryClientProvider>
  );
};

export default App;
