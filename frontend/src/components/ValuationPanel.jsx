import React, { useEffect, useState } from "react"

export default function ValuationPanel({ ticker }) {
  const [valuation, setValuation] = useState(null)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!ticker) return
    fetch(`https://alpha-hub-backend.onrender.com/valuation/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => setValuation(data))
      .catch((err) => {
        console.error("Valuation fetch error:", err)
        setError("Failed to load valuation data.")
      })
  }, [ticker])

  if (!ticker) return null

  return (
    <div className="mt-10 bg-zinc-900 p-6 rounded-2xl shadow-xl ring-1 ring-zinc-800 space-y-8">
      <h2 className="text-2xl font-bold text-purple-300 mb-2">💰 Valuation Dashboard</h2>

      {error && <p className="text-red-400">{error}</p>}
      {!valuation && !error && <p className="text-gray-400">Fetching valuation data...</p>}

      {valuation && (
        <>
          {/* Multiples Section */}
          <section>
            <h3 className="text-lg text-cyan-300 font-semibold mb-2">📊 Comparable Company Multiples</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {valuation.peer_multiples.map((comp, idx) => (
                <div key={idx} className="bg-zinc-800 p-4 rounded-lg border border-zinc-700 space-y-2">
                  <h4 className="text-white font-medium">{comp.name}</h4>
                  <ul className="text-sm text-zinc-400 space-y-1">
                    <li>P/E: {comp.pe.toFixed(2)}</li>
                    <li>EV/EBITDA: {comp.ev_ebitda}</li>
                    <li>EV/Revenue: {comp.ev_sales}</li>
                    <li>Market Cap: ${comp.market_cap.toLocaleString()}</li>
                  </ul>
                </div>
              ))}
            </div>
          </section>

          {/* Precedent Transactions */}
          {valuation.transactions?.length > 0 && (
            <section>
              <h3 className="text-lg text-cyan-300 font-semibold mb-2">🤝 Precedent Transactions</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {valuation.transactions.map((tx, idx) => (
                  <div key={idx} className="bg-zinc-800 p-4 rounded-lg border border-zinc-700 space-y-1">
                    <p>
                      <span className="text-white font-medium">{tx.target}</span> acquired by {tx.acquirer}
                    </p>
                    <ul className="text-sm text-zinc-400 pl-2 space-y-1">
                      <li>EV/Revenue: {tx.ev_rev}</li>
                      <li>EV/EBITDA: {tx.ev_ebitda}</li>
                    </ul>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Valuation Summary */}
          <section>
            <h3 className="text-lg text-cyan-300 font-semibold mb-2">📈 Valuation Summary</h3>
            <div className="bg-zinc-800 p-4 rounded-lg border border-zinc-700 space-y-2 text-sm text-zinc-300">
              <p><span className="text-white font-medium">P/E Implied Equity:</span> ${valuation.valuation_summary.pe_implied_equity.toLocaleString()}</p>
              <p><span className="text-white font-medium">EBITDA-based EV:</span> ${valuation.valuation_summary.ev_ebitda_implied_ev.toLocaleString()}</p>
              <p><span className="text-white font-medium">Sales-based EV:</span> ${valuation.valuation_summary.ev_sales_implied_ev.toLocaleString()}</p>
              <div>
                <span className="text-white font-medium">Implied Share Price Range:</span>
                <ul className="pl-4 space-y-1">
                  <li>• PE-based: ${valuation.valuation_summary.share_price_range.pe_based.toLocaleString()}</li>
                  <li>• EBITDA-based: ${valuation.valuation_summary.share_price_range.ebitda_based.toLocaleString()}</li>
                  <li>• Sales-based: ${valuation.valuation_summary.share_price_range.sales_based.toLocaleString()}</li>
                </ul>
              </div>
            </div>
          </section>

          {/* DCF Section */}
          {valuation.dcf_value && (
            <section>
              <h3 className="text-lg text-green-300 font-semibold mb-2">💡 DCF Valuation Cross-check</h3>
              <p className="text-sm text-zinc-300 bg-zinc-800 p-4 rounded-lg border border-zinc-700">
                Estimated Value (Discounted Cash Flow): ${valuation.dcf_value.toLocaleString()}
              </p>
            </section>
          )}

          {/* Sensitivity Matrix */}
          {valuation.sensitivity_matrix && (
            <section>
              <h3 className="text-lg text-yellow-300 font-semibold mb-2">📊 Valuation Sensitivity Matrix</h3>
              <pre className="text-xs text-zinc-300 bg-zinc-800 p-4 rounded-lg border border-zinc-700 overflow-x-auto">
                {JSON.stringify(valuation.sensitivity_matrix, null, 2)}
              </pre>
            </section>
          )}

          {/* Commentary */}
          {valuation.commentary && (
            <section>
              <h3 className="text-lg text-pink-300 font-semibold mb-2">🧠 Analyst Commentary</h3>
              <p className="text-sm text-zinc-300 italic bg-zinc-800 p-4 rounded-lg border border-zinc-700">
                {valuation.commentary}
              </p>
            </section>
          )}

          {/* Notes */}
          <div className="text-sm text-zinc-400 mt-4 italic">
            <p>Note: Valuation figures are based on latest available data.</p>
            <p>As of: {valuation.as_of_date || "N/A"}</p>
          </div>
        </>
      )}
    </div>
  )
}
