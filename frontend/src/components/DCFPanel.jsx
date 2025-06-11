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
    <div className="mt-10">
      <h2 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-6">
        💡 Discounted Cash Flow (DCF)
      </h2>

      {loading && <p className="text-gray-400">Loading DCF valuation...</p>}
      {error && <p className="text-red-400">{error}</p>}

      {!loading && dcf && (
        <div className="bg-zinc-900 border border-zinc-700 rounded-2xl p-5 transition-all duration-300 ease-in-out hover:border-blue-500 hover:shadow-[0_0_10px_#3b82f6]">
          <p className="text-sm text-blue-400 mb-2">💡 | 📊</p>
          <h3 className="text-lg font-bold text-blue-200 mb-4">DCF Valuation Breakdown</h3>

          <div className="text-sm text-zinc-300 space-y-3">
            <p>
              <span className="text-white font-medium">Discount Rate (WACC):</span> {(dcf.discount_rate * 100).toFixed(2)}%
            </p>
            <p>
              <span className="text-white font-medium">Terminal Growth Rate:</span> {(dcf.terminal_growth_rate * 100).toFixed(2)}%
            </p>
            <p>
              <span className="text-white font-medium">Terminal Value:</span> ${(dcf.terminal_value / 1e9).toFixed(2)}B
            </p>
            <p>
              <span className="text-white font-medium">PV of Free Cash Flows:</span> ${(dcf.present_value_of_fcfs / 1e9).toFixed(2)}B
            </p>
            <p>
              <span className="text-white font-medium">PV of Terminal Value:</span> ${(dcf.present_value_of_terminal / 1e9).toFixed(2)}B
            </p>
            <p className="text-blue-300 font-semibold">
              Total DCF Valuation: ${(dcf.total_dcf_valuation / 1e9).toFixed(2)}B
            </p>

            <div className="mt-4">
              <p className="text-blue-400 font-semibold mb-2">🗓️ Projected Free Cash Flows</p>
              <ul className="list-disc list-inside space-y-1 text-zinc-300">
                {dcf.projected_fcfs.map((fcf, i) => (
                  <li key={i}>Year {i + 1}: ${(fcf / 1e9).toFixed(2)}B</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
