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
    <div className="mt-10">
      <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-sky-300 via-cyan-300 to-blue-200 drop-shadow-lg mb-6 tracking-tight">
        🤝 Deal Radar
      </h2>

      {loading && <p className="text-gray-400">Loading M&A activity...</p>}
      {error && <p className="text-red-400">{error}</p>}
      {!loading && deals.length === 0 && (
        <p className="text-zinc-500 italic">No recent M&A activity found.</p>
      )}

      <div className="overflow-x-auto">
        <div className="flex space-x-4 pb-2">
          {deals.map((deal, idx) => (
            <div
              key={idx}
              className="min-w-[300px] max-w-[300px] bg-zinc-900 border border-zinc-700 rounded-2xl p-5 flex-shrink-0
                         transition-all duration-300 ease-in-out
                         hover:border-blue-500 hover:shadow-[0_0_10px_#3b82f6]"
            >
              <p className="text-sm text-blue-400 mb-3 font-medium">
                #{idx + 1} of {deals.length}
              </p>
              <a
                href={deal.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-lg font-bold text-blue-200 hover:underline leading-snug"
              >
                {deal.title}
              </a>
              <p className="text-sm text-zinc-400 mt-3">
                {deal.published} — {new Date(deal.date).toLocaleDateString()}
              </p>
              <div className="mt-3 text-zinc-500 text-sm">📁 | 🔗</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
