import React, { useState } from "react"

export default function SynergySimulator() {
  const [revenue, setRevenue] = useState(100_000_000)
  const [margin, setMargin] = useState(0.15)
  const [synergies, setSynergies] = useState(20_000_000)
  const [dealCost, setDealCost] = useState(5_000_000)
  const [result, setResult] = useState(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const runSimulation = async () => {
    setLoading(true)
    setError("")
    setResult(null)

    const url = `http://0.0.0.0:10000/synergy/?target_revenue=${revenue}&target_margin=${margin}&expected_synergies=${synergies}&deal_cost=${dealCost}`

    try {
      const res = await fetch(url)
      const data = await res.json()
      setResult(data)
    } catch (err) {
      console.error(err)
      setError("Failed to simulate synergy scenario.")
    }

    setLoading(false)
  }

  return (
    <div className="bg-zinc-900 mt-10 p-6 rounded-xl shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-2xl font-bold text-purple-300 mb-4">📈 Synergy Value Simulator</h2>

      <div className="grid grid-cols-2 gap-4 mb-4 text-zinc-200">
        <label>
          Target Revenue ($):
          <input
            type="number"
            value={revenue}
            onChange={(e) => setRevenue(parseFloat(e.target.value))}
            className="w-full mt-1 p-2 rounded bg-zinc-800 border border-zinc-600"
          />
        </label>

        <label>
          Operating Margin (% as decimal):
          <input
            type="number"
            step="0.01"
            value={margin}
            onChange={(e) => setMargin(parseFloat(e.target.value))}
            className="w-full mt-1 p-2 rounded bg-zinc-800 border border-zinc-600"
          />
        </label>

        <label>
          Expected Synergies ($):
          <input
            type="number"
            value={synergies}
            onChange={(e) => setSynergies(parseFloat(e.target.value))}
            className="w-full mt-1 p-2 rounded bg-zinc-800 border border-zinc-600"
          />
        </label>

        <label>
          Deal Cost ($):
          <input
            type="number"
            value={dealCost}
            onChange={(e) => setDealCost(parseFloat(e.target.value))}
            className="w-full mt-1 p-2 rounded bg-zinc-800 border border-zinc-600"
          />
        </label>
      </div>

      <button
        onClick={runSimulation}
        className="px-4 py-2 bg-purple-700 hover:bg-purple-600 text-white rounded-lg font-semibold transition"
      >
        Run Simulation
      </button>

      {loading && <p className="mt-4 text-gray-400">Calculating...</p>}
      {error && <p className="mt-4 text-red-400">{error}</p>}

      {result && (
        <div className="mt-6 text-zinc-300 space-y-2 text-sm">
          <p><span className="font-semibold text-white">Value Creation:</span> ${result.value_creation.toLocaleString()}</p>
          <p><span className="font-semibold text-white">Summary:</span> {result.summary}</p>
        </div>
      )}
    </div>
  )
}
