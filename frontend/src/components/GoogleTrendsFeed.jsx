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

export default function GoogleTrendsFeed({ ticker }) {
  const [data, setData] = useState(null)
  const [trend, setTrend] = useState("")

  useEffect(() => {
    if (!ticker) return

    fetch(`https://alpha-hub-backend.onrender.com/google/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((d) => {
        console.log("Google Trends data:", d)
        setData(d)
        if (d.interest.length >= 2) {
          const change = d.interest.at(-1) - d.interest.at(-2)
          if (change > 5) setTrend("rising")
          else if (change < -5) setTrend("falling")
          else setTrend("flat")
        }
      })
      .catch((err) => {
        console.error("Google Trends fetch error:", err)
        setData(null)
        setTrend("")
      })
  }, [ticker])

  if (!data) return null

  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: `📈 Google Search Interest (${data.company})`,
        data: data.interest,
        fill: false,
        borderColor: "#38bdf8",
        backgroundColor: "#0ea5e9",
        tension: 0.3
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
      <h2 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-6">
        🔍 Google Trends
      </h2>
      {trend && (
        <div className="text-sm mb-4 text-white">
          Trend:
          {trend === "rising" && (
            <span className="ml-2 text-green-400 font-semibold">📈 Rising</span>
          )}
          {trend === "falling" && (
            <span className="ml-2 text-red-400 font-semibold">📉 Falling</span>
          )}
          {trend === "flat" && (
            <span className="ml-2 text-yellow-400 font-semibold">➖ Stable</span>
          )}
        </div>
      )}
      <Line data={chartData} options={options} />
    </div>
  )
}
