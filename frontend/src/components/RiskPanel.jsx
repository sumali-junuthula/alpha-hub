import React, { useEffect, useState } from "react"

export default function RiskDashboardPanel({ ticker }) {
  const [risks, setRisks] = useState(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!ticker) return

    setLoading(true)
    fetch(`http://0.0.0.0:8000/risk/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        setRisks(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error("Risk fetch error:", err)
        setError("Failed to load risk data.")
        setLoading(false)
      })
  }, [ticker])

  if (!ticker) return null

  const renderRiskSection = (title, risksArray, color) => (
    <div className="mb-6">
      <h3 className={`text-lg font-bold ${color} mb-2`}>{title}</h3>
      <ul className="space-y-2">
        {risksArray.map((r, i) => (
          <li
            key={i}
            className="bg-zinc-800 p-4 rounded-lg border border-zinc-700"
          >
            <p className="text-white font-semibold">{r.title}</p>
            <p className="text-sm text-zinc-400">{r.summary}</p>
            <p className="text-xs text-orange-400 italic mt-1">Impact: {r.impact}</p>
          </li>
        ))}
      </ul>
    </div>
  )

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-rose-300 mb-4">⚠️ Strategic Risk Dashboard</h2>

      {loading && <p className="text-gray-400">Loading risk analysis...</p>}
      {error && <p className="text-red-400">{error}</p>}
      {!loading && risks && (
        <div className="text-sm text-zinc-300 space-y-4">
          {renderRiskSection("Macro Risks", risks.macro_risks, "text-yellow-300")}
          {renderRiskSection("Industry Risks", risks.industry_risks, "text-orange-300")}
          {renderRiskSection("Company Risks", risks.company_risks, "text-rose-300")}

          <div className="bg-zinc-800 p-4 rounded-lg border border-zinc-700">
            <h4 className="text-white font-semibold mb-1">🔎 LLM Summary</h4>
            <p className="text-zinc-400">{risks.llm_generated_risk_summary}</p>
          </div>
        </div>
      )}
    </div>
  )
}
