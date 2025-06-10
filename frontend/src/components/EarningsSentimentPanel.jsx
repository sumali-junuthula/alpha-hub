import React, { useEffect, useState } from "react"

export default function EarningsSentimentPanel({ ticker }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!ticker) return
    setLoading(true)
    setData(null)
    setError("")

    fetch(`http://0.0.0.0:10000/earnings/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((d) => setData(d))
      .catch((err) => {
        console.error("Earnings sentiment fetch error:", err)
        setError("Failed to load earnings sentiment.")
      })
      .finally(() => setLoading(false))
  }, [ticker])

  if (!ticker) return null

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-yellow-300 mb-4">🧾 Earnings Sentiment</h2>

      {loading && <p className="text-gray-400">Analyzing recent earnings headlines...</p>}
      {error && <p className="text-red-400">{error}</p>}

      {data && (
        <>
          <p className="text-zinc-300 mb-3">
            Dominant Sentiment: <span className="font-bold text-white">{data.summary_sentiment}</span> ({data.confidence * 100}% confidence)
          </p>

          <ul className="space-y-3">
            {data.headlines.map((item, idx) => (
              <li
                key={idx}
                className="bg-zinc-800 p-4 rounded-lg border border-zinc-700 hover:border-yellow-500 transition"
              >
                <p className="text-white font-semibold">{item.title}</p>
                <p className="text-sm text-gray-400 mt-1">Sentiment: {item.sentiment}</p>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}
