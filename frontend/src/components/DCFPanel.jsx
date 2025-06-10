import React, { useEffect, useState } from "react"

export default function DCFPanel({ ticker }) {
  const [dcf, setDCF] = useState(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!ticker) return

    setLoading(true)
    fetch(`https://alpha-hub-backend.onrender.com/dcf/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        setDCF(data?.dcf_summary || null)
        setLoading(false)
      })
      .catch((err) => {
        console.error("DCF fetch error:", err)
        setError("Failed to load DCF data.")
        setLoading(false)
      })
  }, [ticker])

  if (!ticker) return null

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-orange-300 mb-4">📊 Discounted Cash Flow (DCF)</h2>

      {loading && <p className="text-gray-400">Loading DCF valuation...</p>}
      {error && <p className="text-red-400">{error}</p>}
      {!loading && dcf && (
        <div className="text-sm text-zinc-300 space-y-2">
          <p><span className="text-white font-semibold">Discount Rate (WACC):</span> {(dcf.discount_rate * 100).toFixed(2)}%</p>
          <p><span className="text-white font-semibold">Terminal Growth Rate:</span> {(dcf.terminal_growth_rate * 100).toFixed(2)}%</p>
          <p><span className="text-white font-semibold">Terminal Value:</span> ${ (dcf.terminal_value / 1e9).toFixed(2) }B</p>
          <p><span className="text-white font-semibold">PV of FCFs:</span> ${ (dcf.present_value_of_fcfs / 1e9).toFixed(2) }B</p>
          <p><span className="text-white font-semibold">PV of Terminal Value:</span> ${ (dcf.present_value_of_terminal / 1e9).toFixed(2) }B</p>
          <p><span className="text-white font-semibold">Total DCF Valuation:</span> ${ (dcf.total_dcf_valuation / 1e9).toFixed(2) }B</p>

          <div className="mt-3">
            <p className="underline mb-1">Projected Free Cash Flows:</p>
            <ul className="list-disc list-inside">
              {dcf.projected_fcfs.map((fcf, i) => (
                <li key={i}>Year {i + 1}: ${(fcf / 1e9).toFixed(2)}B</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
