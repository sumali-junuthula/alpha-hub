import React, { useEffect, useState } from "react"

export default function DealRadarPanel({ ticker }) {
  const [deals, setDeals] = useState([])
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!ticker) return

    setLoading(true)
    fetch(`https://alpha-hub-backend.onrender.com/deals/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        setDeals(data.deals || [])
        setLoading(false)
      })
      .catch((err) => {
        console.error("Deal fetch error:", err)
        setError("Failed to load deal data.")
        setLoading(false)
      })
  }, [ticker])

  if (!ticker) return null

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-emerald-300 mb-4">🤝 M&A Deal Radar</h2>

      {loading && <p className="text-gray-400">Loading M&A activity...</p>}
      {error && <p className="text-red-400">{error}</p>}
      {!loading && deals.length === 0 && (
        <p className="text-zinc-400">No recent M&A activity found.</p>
      )}

      <ul className="space-y-3">
        {deals.map((deal, idx) => (
          <li
            key={idx}
            className="bg-zinc-800 p-4 rounded-lg border border-zinc-700 hover:border-emerald-500 transition"
          >
            <a
              href={deal.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-white font-semibold hover:underline"
            >
              {deal.title}
            </a>
            <p className="text-sm text-gray-400 mt-1">{deal.published} — {new Date(deal.date).toLocaleDateString()}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}
