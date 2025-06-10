import React, { useEffect, useState } from "react"
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from "recharts"

export default function CompetitiveHeatmap({ ticker }) {
  const [data, setData] = useState([])
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!ticker) return

    setLoading(true)
    fetch(`http://0.0.0.0:10000/positioning/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((json) => {
        setData(json.metrics || [])
        setLoading(false)
      })
      .catch((err) => {
        console.error("Heatmap fetch error:", err)
        setError("Failed to load positioning data.")
        setLoading(false)
      })
  }, [ticker])

  if (!ticker) return null

  return (
    <div className="bg-zinc-900 mt-10 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-sky-300 mb-4">🧭 Competitive Positioning</h2>

      {loading && <p className="text-gray-400">Loading heatmap...</p>}
      {error && <p className="text-red-400">{error}</p>}

      {!loading && data.length > 0 && (
        <div style={{ width: "100%", height: 400 }}>
          <ResponsiveContainer>
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
              <PolarGrid />
              <PolarAngleAxis dataKey="metric" tick={{ fill: "#ccc" }} />
              <PolarRadiusAxis tick={{ fill: "#999" }} />
              <Radar
                name="Positioning"
                dataKey="score"
                stroke="#38bdf8"
                fill="#38bdf8"
                fillOpacity={0.6}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
