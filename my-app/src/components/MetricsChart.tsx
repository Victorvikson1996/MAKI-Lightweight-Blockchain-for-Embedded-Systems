import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

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

interface MetricsChartProps {
  metrics: Metric[];
}

const MetricsChart: React.FC<MetricsChartProps> = ({ metrics }) => {
  const labels = metrics.map((metric) => `PID: ${metric.pid}`);
  const cpuData = metrics.map((metric) => metric.cpu_usage);
  const memoryData = metrics.map((metric) => metric.memory_percent);

  const data = {
    labels,
    datasets: [
      {
        label: 'CPU Usage (%)',
        data: cpuData,
        backgroundColor: 'rgba(75, 192, 192, 0.6)'
      },
      {
        label: 'Memory Usage (%)',
        data: memoryData,
        backgroundColor: 'rgba(153, 102, 255, 0.6)'
      }
    ]
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        stacked: true
      },
      y: {
        stacked: true,
        beginAtZero: true
      }
    },
    plugins: {
      legend: {
        position: 'bottom' as const
      },
      title: {
        display: true,
        text: 'Agent Metrics'
      }
    }
  };

  return <Bar data={data} options={options} />;
};

export default MetricsChart;
