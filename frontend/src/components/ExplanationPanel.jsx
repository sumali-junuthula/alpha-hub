import React, { useEffect, useState } from "react"

export default function ExplainPanel({ ticker }) {
  const [explanation, setExplanation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!ticker) return

    setLoading(true)
    fetch(`http://0.0.0.0:8000/explainer/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        setExplanation(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error("Explain fetch error:", err)
        setError("Failed to load explanation.")
        setLoading(false)
      })
  }, [ticker])

  if (!ticker) return null

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-purple-300 mb-4">🧠 Forecast Explanation</h2>

      {loading && <p className="text-gray-400">Generating explanation...</p>}
      {error && <p className="text-red-400">{error}</p>}
      
      {explanation && (
        <div className="text-zinc-300 space-y-4">
          <p className="text-white text-md italic">"{explanation.summary}"</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
            {explanation.explanations.map((item, idx) => (
              <div
                key={idx}
                className="bg-zinc-800 p-4 rounded-lg border border-zinc-700"
              >
                <p className="text-white font-semibold">{item.source}</p>
                <p className="text-sm text-gray-400 mt-1">{item.summary}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
