import React, { useEffect, useState } from "react"
import { Line } from "react-chartjs-2"
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend
} from "chart.js"

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend
)

export default function SatelliteSignalFeed({ ticker }) {
  const [data, setData] = useState(null)

  useEffect(() => {
    if (!ticker) return

    fetch(`http://0.0.0.0:8000/satellite/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((d) => setData(d))
      .catch((err) => {
        console.error("Satellite fetch error:", err)
        setData(null)
      })
  }, [ticker])

  if (!data) return null

  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: `📡 ${data.metric} (${data.ticker})`,
        data: data.signal,
        borderColor: "#38bdf8",
        backgroundColor: "#0ea5e9",
        fill: false,
        tension: 0.3,
        pointBorderColor: "#7dd3fc",
        pointBackgroundColor: "#7dd3fc"
      }
    ]
  }

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { mode: "index", intersect: false }
    },
    scales: {
      y: {
        ticks: { color: "#7dd3fc" },
        grid: { color: "#334155" }
      },
      x: {
        ticks: { color: "#7dd3fc" },
        grid: { color: "#1e293b" }
      }
    }
  }

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-cyan-300 mb-4">
        📡 Satellite Activity Signal (Simulated)
      </h2>
      <Line data={chartData} options={options} />
    </div>
  )
}
