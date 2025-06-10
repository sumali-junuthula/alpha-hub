import React, { useState, useEffect } from "react"
import ForecastGraph from "../components/ForecastGraph"
import NewsFeed from "../components/NewsFeed"
import RedditFeed from "../components/RedditFeed"
import GoogleTrendsFeed from "../components/GoogleTrendsFeed"
import CompetitorSignalFeed from "../components/CompetitorSignalFeed"
import SatelliteSignalFeed from "../components/SatelliteSignalFeed"
import ValuationPanel from "../components/ValuationPanel"
import DealRadarPanel from "../components/DealRadarPanel"
import EarningsSentimentPanel from "../components/EarningsSentimentPanel"
import DCFPanel from "../components/DCFPanel"
import RiskPanel from "../components/RiskPanel"
import SynergySimulator from "../components/SynergySimulator"
import CompetitiveHeatmap from "../components/CompetitiveHeatmap"
import SectorPanel from "../components/SectorPanel"
import ExplanationPanel from "../components/ExplanationPanel"
import StrategyPanel from "../components/StrategyPanel"

export default function Dashboard() {
  const [input, setInput] = useState("")
  const [ticker, setTicker] = useState("")
  const [forecast, setForecast] = useState(null)
  const [company, setCompany] = useState(null)
  const [error, setError] = useState("")
  const [redditPosts, setRedditPosts] = useState([])

  const temp_link = "http://0.0.0.0:8000"

  const handleSearch = () => {
    if (!input) return

    setTicker("")
    setForecast(null)
    setCompany(null)
    setError("")
    setRedditPosts([])

    fetch(`${temp_link}/resolve/?query=${input}`)
      .then((res) => res.json())
      .then((resolveData) => {
        const resolvedTicker = resolveData.resolved?.toUpperCase()
        
        if (!resolvedTicker) {
          setError("Invalid company or ticker")
          return
        }
        
        setTicker(resolvedTicker)

        // fetch(`${temp_link}/company/?ticker=${resolvedTicker}`)
        //   .then((res) => res.json())
        //   .then((metaData) => setCompany(metaData))
        //   .catch((err) => {
        //     console.error("Company metadata fetch error:", err)
        //   })

        fetch(`${temp_link}/forecast/?ticker=${resolvedTicker}`)
          .then((res) => res.json())
          .then((data) => {
            console.log("Forecast data:", data)
            setForecast(data)
          })
          .catch((err) => {
            console.error(err)
            setError("Error fetching forecast data.")
          })

        fetch(`${temp_link}/reddit/?ticker=${resolvedTicker}`)
          .then((res) => res.json())
          .then((data) => setRedditPosts(data))
      })
      .catch((err) => {
        console.error("Resolve error:", err)
        setError("Could not resolve company name to ticker.")
      })
  }

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center px-4">
      <div className="backdrop-blur-sm bg-white/5 border border-gray-700 shadow-xl rounded-2xl p-10 max-w-2xl w-full">
        <h1 className="text-5xl font-extrabold text-center mb-6 bg-gradient-to-r from-indigo-400 via-sky-500 to-teal-400 bg-clip-text text-transparent drop-shadow-md tracking-tight">
          AlphaHub
        </h1>

        <div className="flex items-center w-full bg-zinc-800 rounded-lg shadow-sm ring-1 ring-zinc-700 focus-within:ring-2 focus-within:ring-blue-500 transition mb-6">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Please enter a ticker"
            className="flex-1 bg-transparent px-4 py-3 text-white placeholder-zinc-400 outline-none"
          />
          <button
            onClick={handleSearch}
            className="px-5 py-3 text-white font-medium bg-blue-600 hover:bg-blue-700 rounded-r-lg transition"
          >
            Search
          </button>
        </div>

        <div className="h-1 w-full bg-gradient-to-r from-green-400 via-blue-500 to-purple-600 animate-pulse rounded-full mb-6"></div>

        {forecast ? (
          <div className="mt-10 space-y-8">
            <ForecastGraph key={ticker} forecast={forecast} />
            <StrategyPanel strategy={forecast.strategy} />
            <GoogleTrendsFeed ticker={ticker} />
            <ValuationPanel ticker={ticker} />
            <DealRadarPanel ticker={ticker} />
            <DCFPanel ticker={ticker} />
            <RiskPanel ticker={ticker} />
            <SynergySimulator />
            <CompetitiveHeatmap ticker={ticker} />
            {company?.industry && <SectorPanel sector={company.industry} />}
            <ExplanationPanel ticker={ticker} />
            <RedditFeed posts={redditPosts} />
            <NewsFeed ticker={ticker} />
          </div>
        ) : (
          <p className="text-center text-gray-400">No data yet — please enter a ticker.</p>
        )}
      </div>
    </div>
  )
}
