import React, { useState } from "react";
import ForecastGraph from "../components/ForecastGraph";

export default function Dashboard() {
  const [ticker, setTicker] = useState("");
  const [forecast, setForecast] = useState(null);
  const [error, setError] = useState("");

  const handleSearch = () => {
    if (!ticker) return;
    fetch(`https://refactored-goldfish-pj94qqjqvrgwh94jg-8000.app.github.dev/forecast/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Forecast data:", data); // 👈 Add this
        setForecast(data);
      })
      // .then((data) => setForecast(data.forecast))
      .catch((err) => {
        console.error(err);
        setError("Error fetching forecast data.");
      });
  };

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center px-4">
      <div className="backdrop-blur-sm bg-white/5 border border-gray-700 shadow-xl rounded-2xl p-10 max-w-2xl w-full">
        <h1 className="text-5xl font-extrabold text-center mb-6 bg-gradient-to-r from-indigo-400 via-sky-500 to-teal-400 bg-clip-text text-transparent drop-shadow-md tracking-tight">
          AlphaHub
        </h1>

        <div className="flex items-center w-full bg-zinc-800 rounded-lg shadow-sm ring-1 ring-zinc-700 focus-within:ring-2 focus-within:ring-blue-500 transition mb-6">
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="Search for a company or ticker"
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
          <div className="mt-10">
            <ForecastGraph forecast={forecast} />
          </div>
        ) : (
          <p className="text-center text-gray-400">No data yet — please enter a ticker.</p>
        )}
      </div>
    </div>
  );
}
