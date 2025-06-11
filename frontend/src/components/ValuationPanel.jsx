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
    <div className="mt-10">
      <h2 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-6">
        💰 Valuation Overview
      </h2>

      {error && <p className="text-red-400">{error}</p>}
      {!valuation && !error && <p className="text-gray-400">Loading valuation data...</p>}

      {valuation && (
        <div className="flex flex-col space-y-6">
          {/* Card Component */}
          {[
            {
              icon: "📊 | 🔍",
              title: "Comparable Company Multiples",
              content: valuation.peer_multiples.map((comp, idx) => (
                <div key={idx}>
                  <p className="text-white font-semibold">{comp.name}</p>
                  <ul className="text-sm text-zinc-400 pl-3 space-y-1">
                    <li>P/E: {comp.pe.toFixed(2)}</li>
                    <li>EV/EBITDA: {comp.ev_ebitda}</li>
                    <li>EV/Revenue: {comp.ev_sales}</li>
                    <li>Market Cap: ${comp.market_cap.toLocaleString()}</li>
                  </ul>
                </div>
              ))
            },
            {
              icon: "🤝 | 📁",
              title: "Precedent Transactions",
              content: valuation.transactions?.length
                ? valuation.transactions.map((tx, idx) => (
                    <div key={idx}>
                      <p className="text-white font-semibold">{tx.target}</p>
                      <p className="text-sm text-zinc-400">Acquired by {tx.acquirer}</p>
                      <ul className="text-sm text-zinc-400 pl-3 space-y-1">
                        <li>EV/Revenue: {tx.ev_rev}</li>
                        <li>EV/EBITDA: {tx.ev_ebitda}</li>
                      </ul>
                    </div>
                  ))
                : <p className="text-sm text-zinc-400">No recent deals found.</p>
            },
            {
              icon: "📈 | 💵",
              title: "Valuation Summary",
              content: (
                <ul className="text-sm text-zinc-300 space-y-2">
                  <li><span className="text-white font-medium">P/E Implied Equity:</span> ${valuation.valuation_summary.pe_implied_equity.toLocaleString()}</li>
                  <li><span className="text-white font-medium">EBITDA-based EV:</span> ${valuation.valuation_summary.ev_ebitda_implied_ev.toLocaleString()}</li>
                  <li><span className="text-white font-medium">Sales-based EV:</span> ${valuation.valuation_summary.ev_sales_implied_ev.toLocaleString()}</li>
                  <li>
                    <span className="text-white font-medium">Implied Share Price Range:</span>
                    <ul className="pl-4 space-y-1">
                      <li>• PE-based: ${valuation.valuation_summary.share_price_range.pe_based.toLocaleString()}</li>
                      <li>• EBITDA-based: ${valuation.valuation_summary.share_price_range.ebitda_based.toLocaleString()}</li>
                      <li>• Sales-based: ${valuation.valuation_summary.share_price_range.sales_based.toLocaleString()}</li>
                    </ul>
                  </li>
                </ul>
              )
            },
            valuation.dcf_value && {
              icon: "💡 | 📊",
              title: "DCF Valuation",
              content: (
                <p className="text-sm text-zinc-300">
                  Estimated Value (Discounted Cash Flow): ${valuation.dcf_value.toLocaleString()}
                </p>
              )
            },
            valuation.sensitivity_matrix && {
              icon: "🧪 | 🔬",
              title: "Sensitivity Matrix",
              content: (
                <div className="bg-zinc-900 border border-zinc-700 rounded-2xl p-5 transition-all duration-300 ease-in-out hover:border-blue-500 hover:shadow-[0_0_10px_#3b82f6]">
                  <p className="text-sm text-blue-400 mb-2">🧪 | 🔬</p>
                  <h3 className="text-lg font-bold text-blue-200 mb-4">Sensitivity Matrix</h3>

                  <div className="overflow-x-auto">
                    <table className="min-w-full text-sm text-zinc-300 border-collapse">
                      <thead>
                        <tr className="text-blue-300 border-b border-zinc-700">
                          <th className="px-3 py-2 text-left">Metric</th>
                          {Object.keys(valuation.sensitivity_matrix[0]).filter(key => key !== "metric").map((col, idx) => (
                            <th key={idx} className="px-3 py-2 text-left">{col}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {valuation.sensitivity_matrix.map((row, idx) => (
                          <tr key={idx} className="border-b border-zinc-800 hover:bg-zinc-800/50">
                            <td className="px-3 py-2 font-medium text-white">{row.metric}</td>
                            {Object.keys(row).filter(k => k !== "metric").map((k, i) => (
                              <td key={i} className="px-3 py-2">{row[k]}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )
            },
            valuation.commentary && {
              icon: "🧠 | 📌",
              title: "Analyst Commentary",
              content: (
                <p className="text-sm text-zinc-300 italic">{valuation.commentary}</p>
              )
            }
          ].filter(Boolean).map((section, idx) => (
            <div
              key={idx}
              className="bg-zinc-900 border border-zinc-700 rounded-2xl p-5 transition-all duration-300 ease-in-out hover:border-blue-500 hover:shadow-[0_0_10px_#3b82f6]"
            >
              <p className="text-sm text-blue-400 mb-2">{section.icon}</p>
              <h3 className="text-lg font-bold text-blue-200 mb-3">{section.title}</h3>
              {section.content}
            </div>
          ))}

          {/* Footer Note */}
          <div className="text-sm text-zinc-500 mt-2 italic">
            As of: {valuation.as_of_date || "N/A"}
          </div>
        </div>
      )}
    </div>
  )
}
