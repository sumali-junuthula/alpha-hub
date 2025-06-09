import React, { useEffect, useState } from "react"

export default function SectorCommentaryPanel({ sector }) {
  const [commentary, setCommentary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!sector) return

    setLoading(true)
    fetch(`http://0.0.0.0:8000/sector/?sector=${sector}`)
      .then((res) => res.json())
      .then((data) => {
        setCommentary(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error("Sector fetch error:", err)
        setError("Failed to load sector commentary.")
        setLoading(false)
      })
  }, [sector])

  if (!sector) return null

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-yellow-300 mb-4">🌐 Sector Commentary</h2>

      {loading && <p className="text-gray-400">Loading sector insights...</p>}
      {error && <p className="text-red-400">{error}</p>}

      {commentary && (
        <div className="space-y-2 text-sm text-zinc-300">
          <p><span className="text-white font-semibold">Summary:</span> {commentary.summary}</p>
          <p><span className="text-white font-semibold">Key Risks:</span> {commentary.risks}</p>
          <p><span className="text-white font-semibold">Outlook:</span> {commentary.outlook}</p>
        </div>
      )}
    </div>
  )
}
