import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

ChartJS.register(
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Filler
);

export default function ForecastGraph({ forecast }) {
  if (!forecast || !forecast.dates || !forecast.prices) {
    return <p className="text-center text-gray-400">No graph data available.</p>;
  }

  const formattedDates = forecast.dates.map((d) => {
    const date = new Date(d);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    });
  });

  const avgPrice = forecast.prices.reduce((sum, val) => sum + val, 0) / forecast.prices.length;

  const data = {
    labels: formattedDates,
    datasets: [
      {
        label: "Predicted Price",
        data: forecast.prices,
        borderColor: "#3b82f6", // Tailwind blue-500
        backgroundColor: "rgba(59,130,246,0.2)",
        fill: true,
        tension: 0.3,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
      {
        label: "Avg Forecast",
        data: Array(forecast.prices.length).fill(avgPrice),
        borderDash: [8, 5],
        borderColor: "rgba(255, 255, 255, 0.4)",
        borderWidth: 2,
        pointRadius: 0,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: "white",
          boxWidth: 12,
          padding: 20,
        },
      },
      tooltip: {
        mode: "index",
        intersect: false,
        backgroundColor: "#111827", // zinc-900
        titleColor: "#ffffff",
        bodyColor: "#d1d5db",
        borderColor: "#374151", // zinc-700
        borderWidth: 1,
        padding: 10,
      },
    },
    scales: {
      x: {
        ticks: {
          color: "#d1d5db",
        },
        grid: {
          color: "rgba(255,255,255,0.05)",
        },
      },
      y: {
        ticks: {
          color: "#d1d5db",
        },
        grid: {
          color: "rgba(255,255,255,0.05)",
        },
      },
    },
  };

  return (
    <div className="bg-zinc-900 rounded-xl p-6 mt-8 shadow-lg ring-1 ring-zinc-700">
      <Line data={data} options={options} />
    </div>
  );
}
