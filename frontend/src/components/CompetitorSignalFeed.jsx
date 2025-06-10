import React, { useEffect, useState } from "react"
import { motion } from "framer-motion"

export default function CompetitorSignalFeed({ ticker }) {
  const [competitors, setCompetitors] = useState([])
  const [industry, setIndustry] = useState("")
  const [error, setError] = useState("")

  useEffect(() => {
    if (!ticker) return
    fetch(`https://alpha-hub-backend.onrender.com/competitors/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        setCompetitors(data.competitors)
        setIndustry(data.industry)
        setError("")
      })
      .catch((err) => {
        console.error(err)
        setError("Failed to load competitor data.")
      })
  }, [ticker])

  if (!ticker || competitors.length === 0) return null

  return (
    <div className="mt-10">
      <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 via-sky-300 to-blue-200 drop-shadow mb-4">
        🏢 Competitor Overview ({industry})
      </h2>
      {error && <p className="text-red-400">{error}</p>}

      <div className="relative overflow-x-auto snap-x snap-mandatory flex gap-6 pb-2 px-1 scroll-smooth">
        {competitors.map((comp, idx) => (
          <motion.div
            key={idx}
            className="snap-center min-w-[80%] md:min-w-[60%] lg:min-w-[40%] bg-zinc-900 border border-blue-500/30 hover:border-blue-400 transition rounded-2xl p-6 text-white shadow-[0_0_30px_rgba(59,130,246,0.1)]"
            whileHover={{ scale: 1.05, boxShadow: "0 0 60px rgba(59,130,246,0.3)" }}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 80, damping: 18 }}
            viewport={{ once: true }}
          >
            <h3 className="text-lg font-bold text-blue-300 mb-1">{comp.name}</h3>
            <p className="text-sm text-zinc-400 mb-1">Ticker: {comp.ticker} | Exchange: {comp.exchange}</p>
            <p className="text-lg text-cyan-300 font-semibold">
              Price: ${comp.price} ({comp.changesPercentage})
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
