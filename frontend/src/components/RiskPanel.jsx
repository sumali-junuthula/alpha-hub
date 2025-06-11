import React, { useEffect, useState } from "react"

export default function RiskPanel({ ticker }) {
  const [risks, setRisks] = useState(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!ticker) return

    setLoading(true)
    fetch(`https://alpha-hub-backend.onrender.com/risks/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        const formatRisks = (sectionKey) => {
          const section = data[sectionKey]
          if (!section || typeof section !== "object") return []

          return Object.values(section).map(([_, riskObj]) => ({
            title: riskObj.Title || "Untitled",
            summary: riskObj.Description || "No description provided."
          }))
        }

        const parsedRisks = {
          macro_risks: formatRisks("Macroeconomic_Risks"),
          industry_risks: formatRisks("Industry_Risks"),
          company_risks: formatRisks("Company_Risks"),
          llm_generated_risk_summary: data["LLM-Summary"] || "No summary available."
        }

        // console.log(parsedRisks)

        setRisks(parsedRisks)
        setLoading(false)
      })
      .catch((err) => {
        console.error("Risk fetch error:", err)
        setError("Failed to load risk data.")
        setLoading(false)
      })
  }, [ticker])

  if (!ticker) return null

  const renderRiskSection = (title, risksArray = [], color) => (
    <div className="bg-zinc-900 border border-zinc-700 rounded-2xl p-5 transition-all duration-300 ease-in-out hover:border-blue-500 hover:shadow-[0_0_10px_#3b82f6] mb-4">
      <h3 className={`text-lg font-bold ${color} mb-3`}>{title}</h3>
      <ul className="space-y-3">
        {risksArray.map((r, i) => (
          <li key={i} className="bg-zinc-800 p-4 rounded-lg border border-zinc-700">
            <p className="text-white font-semibold">{r.title}</p>
            <p className="text-sm text-zinc-400 mt-1">{r.summary}</p>
            <p className="text-xs text-blue-400 italic mt-2">Impact: {r.impact}</p>
          </li>
        ))}
      </ul>
    </div>
  )

  return (
    <div className="mt-10">
      <h2 className="text-3xl font-bold bg-gradient-to-r from-rose-400 to-red-500 bg-clip-text text-transparent mb-6">
        ⚠️ Strategic Risk Dashboard
      </h2>

      {loading && <p className="text-gray-400">Loading risk analysis...</p>}
      {error && <p className="text-red-400">{error}</p>}
      {!loading && risks && (
        <div className="text-sm text-zinc-300 space-y-6">
          {renderRiskSection("Macro Risks", risks?.macro_risks || [], "text-yellow-300")}
          {renderRiskSection("Industry Risks", risks?.industry_risks || [], "text-orange-300")}
          {renderRiskSection("Company Risks", risks?.company_risks || [], "text-rose-300")}

          <div className="bg-zinc-900 border border-zinc-700 rounded-2xl p-5 transition-all duration-300 ease-in-out hover:border-blue-500 hover:shadow-[0_0_10px_#3b82f6]">
            <p className="text-sm text-blue-400 mb-2">🔎 | Summary</p>
            <h4 className="text-lg font-bold text-blue-200 mb-2">LLM Summary</h4>
            <p className="text-sm text-zinc-300 italic">
              {risks?.llm_generated_risk_summary || "No summary available."}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
