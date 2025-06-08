import React, { useEffect, useState } from "react";

export default function NewsFeed({ ticker }) {
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ticker) return;
    setArticles([]); // reset
    fetch(`https://refactored-goldfish-pj94qqjqvrgwh94jg-8000.app.github.dev/news/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setArticles(data.slice(0, 5)); // top 5
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
    <div className="bg-zinc-900 rounded-xl p-6 mt-8 shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
        🗞️ Latest News
      </h2>
      {error && <p className="text-red-400">{error}</p>}
      {articles.length === 0 && !error && (
        <p className="text-gray-400">No news available.</p>
      )}
      <ul className="space-y-4">
        {articles.map((article, index) => (
          <li key={index} className="border-b border-zinc-800 pb-4">
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:underline text-lg font-medium"
            >
              {article.title}
            </a>
            <p className="text-sm text-gray-400 mt-1">{article.description}</p>
            <p className="text-xs text-zinc-500 mt-1">
              {new Date(article.date).toLocaleDateString()}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
