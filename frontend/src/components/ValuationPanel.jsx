import React, { useEffect, useState } from "react"

export default function ValuationPanel({ ticker }) {
  const [valuation, setValuation] = useState(null)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!ticker) return
    fetch(`http://0.0.0.0:8000/valuation/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => setValuation(data))
      .catch((err) => {
        console.error("Valuation fetch error:", err)
        setError("Failed to load valuation data.")
      })
  }, [ticker])

  if (!ticker) return null

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-purple-300 mb-4">💰 Valuation Overview</h2>

      {error && <p className="text-red-400">{error}</p>}
      {!valuation && !error && <p className="text-gray-400">Loading valuation data...</p>}

      {valuation && (
        <>
          {/* Multiples Section */}
          <div className="mb-6">
            <h3 className="text-lg text-cyan-300 font-semibold mb-2">📊 Comparable Company Multiples</h3>
            <ul className="space-y-2 text-sm text-zinc-300">
              {valuation.peer_multiples.map((comp, idx) => (
                <li key={idx} className="border-b border-zinc-700 pb-2">
                  <span className="text-white font-medium">{comp.name}</span>
                  <ul className="text-zinc-400 text-sm pl-4">
                    <li>P/E: {comp.pe.toFixed(2)}</li>
                    <li>EV/EBITDA: {comp.ev_ebitda}</li>
                    <li>EV/Revenue: {comp.ev_sales}</li>
                    <li>Market Cap: ${comp.market_cap.toLocaleString()}</li>
                  </ul>
                </li>
              ))}
            </ul>
          </div>

          {/* Precedent Transactions Section */}
          {valuation.transactions && valuation.transactions.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg text-cyan-300 font-semibold mb-2">🤝 Precedent Transactions</h3>
              <ul className="space-y-2 text-sm text-zinc-300">
                {valuation.transactions.map((tx, idx) => (
                  <li key={idx} className="border-b border-zinc-700 pb-2">
                    <span className="text-white font-medium">{tx.target}</span> acquired by {tx.acquirer}
                    <ul className="text-zinc-400 text-sm pl-4">
                      <li>EV/Revenue: {tx.ev_rev}</li>
                      <li>EV/EBITDA: {tx.ev_ebitda}</li>
                    </ul>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Valuation Summary Section */}
          <div className="mb-6">
            <h3 className="text-lg text-cyan-300 font-semibold mb-2">📈 Valuation Summary</h3>
            <ul className="space-y-2 text-sm text-zinc-300">
              <li><span className="text-white font-medium">P/E Implied Equity:</span> ${valuation.valuation_summary.pe_implied_equity.toLocaleString()}</li>
              <li><span className="text-white font-medium">EBITDA-based EV:</span> ${valuation.valuation_summary.ev_ebitda_implied_ev.toLocaleString()}</li>
              <li><span className="text-white font-medium">Sales-based EV:</span> ${valuation.valuation_summary.ev_sales_implied_ev.toLocaleString()}</li>
              <li>
                <span className="text-white font-medium">Implied Share Price Range:</span>
                <ul className="pl-4">
                  <li>• PE-based: ${valuation.valuation_summary.share_price_range.pe_based.toLocaleString()}</li>
                  <li>• EBITDA-based: ${valuation.valuation_summary.share_price_range.ebitda_based.toLocaleString()}</li>
                  <li>• Sales-based: ${valuation.valuation_summary.share_price_range.sales_based.toLocaleString()}</li>
                </ul>
              </li>
            </ul>
          </div>

          {/* Optional Features Section */}
          {valuation.dcf_value && (
            <div className="mb-6">
              <h3 className="text-lg text-green-300 font-semibold mb-2">💡 DCF Valuation Cross-check</h3>
              <p className="text-sm text-zinc-300">Estimated Value (Discounted Cash Flow): ${valuation.dcf_value.toLocaleString()}</p>
            </div>
          )}

          {valuation.sensitivity_matrix && (
            <div className="mb-6">
              <h3 className="text-lg text-yellow-300 font-semibold mb-2">📊 Valuation Sensitivity Matrix</h3>
              <pre className="text-xs text-zinc-300 bg-zinc-800 p-3 rounded-md overflow-x-auto">
                {JSON.stringify(valuation.sensitivity_matrix, null, 2)}
              </pre>
            </div>
          )}

          {valuation.commentary && (
            <div className="mb-6">
              <h3 className="text-lg text-pink-300 font-semibold mb-2">🧠 Analyst Commentary</h3>
              <p className="text-sm text-zinc-300 italic">{valuation.commentary}</p>
            </div>
          )}

          {/* Optional Notes */}
          <div className="text-sm text-zinc-400 mt-4 italic">
            <p>Note: Valuation multiples are based on the most recent data available.</p>
            <p>As of: {valuation.as_of_date || "N/A"}</p>
          </div>
        </>
      )}
    </div>
  )
}
