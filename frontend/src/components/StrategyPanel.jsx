import React from "react"
import { Line } from "react-chartjs-2"
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from "chart.js"

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
)

export default function StrategyPanel({ strategy }) {
  if (!strategy || !strategy.dates || !strategy.prices) return null

  const { dates, prices, signals, metrics } = strategy

  const buySignals = dates.map((date, i) =>
    signals[i] === "BUY" ? prices[i] : null
  )
  const sellSignals = dates.map((date, i) =>
    signals[i] === "SELL" ? prices[i] : null
  )

  const chartData = {
    labels: dates,
    datasets: [
      {
        label: "Price",
        data: prices,
        borderColor: "#38bdf8",
        fill: false,
        tension: 0.3
      },
      {
        label: "Buy",
        data: buySignals,
        borderColor: "#4ade80",
        backgroundColor: "#4ade80",
        pointRadius: 5,
        type: "scatter",
        showLine: false
      },
      {
        label: "Sell",
        data: sellSignals,
        borderColor: "#f87171",
        backgroundColor: "#f87171",
        pointRadius: 5,
        type: "scatter",
        showLine: false
      }
    ]
  }

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { mode: "index", intersect: false }
    },
    scales: {
      y: {
        ticks: { color: "#94a3b8" },
        grid: { color: "#334155" }
      },
      x: {
        ticks: { color: "#94a3b8" },
        grid: { display: false }
      }
    }
  }

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-blue-300 mb-4">📊 Backtested Strategy Performance</h2>
      <Line data={chartData} options={options} />
      <div className="mt-4 text-sm text-zinc-300 space-y-1">
        <p><span className="text-white font-semibold">Total Return:</span> {metrics?.return_pct}%</p>
        <p><span className="text-white font-semibold">Sharpe Ratio:</span> {metrics?.sharpe}</p>
        <p><span className="text-white font-semibold">Trades Executed:</span> {metrics?.trades}</p>
      </div>
    </div>
  )
}
