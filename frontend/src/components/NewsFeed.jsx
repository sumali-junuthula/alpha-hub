// src/components/NewsFeed.jsx
import React, { useEffect, useState } from "react";

export default function NewsFeed({ ticker }) {
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ticker) return;
    setArticles([]);
    fetch(`https://refactored-goldfish-pj94qqjqvrgwh94jg-8000.app.github.dev/news/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setArticles(data.slice(0, 6));
        } else {
          throw new Error("Unexpected format");
        }
      })
      .catch((err) => {
        console.error("News fetch error:", err);
        setError("Failed to load news.");
      });
  }, [ticker]);

  return (
    <div className="mt-12">
      <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">🗞️ Latest News</h2>

      {error && <p className="text-red-400">{error}</p>}
      {!error && articles.length === 0 && (
        <p className="text-gray-400">No news available for this ticker.</p>
      )}

      <div className="flex gap-6 overflow-x-auto pb-4 scroll-smooth">
        {articles.map((article, index) => (
          <div
            key={index}
            className="min-w-[320px] max-w-[320px] flex-shrink-0 bg-zinc-900 border border-zinc-700 rounded-xl shadow-lg overflow-hidden hover:scale-[1.02] transition-transform"
          >
            {article.image && (
              <img
                src={article.image}
                alt={article.title}
                className="w-full h-40 object-cover"
              />
            )}
            <div className="p-4 flex flex-col justify-between h-[220px]">
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-lg font-semibold text-blue-400 hover:underline"
              >
                {article.title.length > 60 ? article.title.slice(0, 60) + "..." : article.title}
              </a>
              <p className="text-sm text-gray-400 mt-2 line-clamp-3">
                {article.description || "No description."}
              </p>
              <p className="text-xs text-zinc-500 mt-auto pt-4">
                {new Date(article.date).toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                  year: "numeric",
                })}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
