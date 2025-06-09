import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

export default function NewsFeed({ ticker }) {
  const [articles, setArticles] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ticker) return;
    setArticles([]); // reset
    fetch(`http://0.0.0.0:8000/news/?ticker=${ticker}`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setArticles(data); // show all
        } else {
          throw new Error("Unexpected format");
        }
      })
      .catch((err) => {
        console.error("News fetch error:", err);
        setError("Failed to load news.");
      });
  }, [ticker]);

  if (!ticker) return null;

  return (
    <div className="mt-14">
      {/* Gradient Header */}
      <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-sky-300 via-cyan-300 to-blue-200 drop-shadow-lg mb-6 tracking-tight">
        🗞️ Latest News
      </h2>

      {error && <p className="text-red-400">{error}</p>}
      {articles.length === 0 && !error && (
        <p className="text-gray-400">No news available.</p>
      )}

      <div className="overflow-x-auto snap-x snap-mandatory flex gap-6 px-4 pb-2 scroll-smooth scrollbar-thin scrollbar-thumb-zinc-700">
        {articles.map((article, idx) => (
          <motion.a
            key={idx}
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="snap-center bg-zinc-900 border border-blue-500/30 hover:border-blue-400 transition rounded-2xl p-6 text-white min-w-[80%] md:min-w-[60%] lg:min-w-[45%] cursor-pointer shadow-md"
            whileHover={{
              scale: 1.02,
              boxShadow: "0 0 20px rgba(59,130,246,0.25)",
            }}
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: idx * 0.1 }}
            viewport={{ once: true }}
          >
            <h3 className="text-lg font-bold text-blue-300 mb-2">
              {article.title}
            </h3>
            <p className="text-zinc-400 text-sm mb-2">
              {article.description || "No summary available."}
            </p>
            <p className="text-xs text-zinc-500">
              {new Date(article.date).toLocaleDateString()}
            </p>
          </motion.a>
        ))}
      </div>
    </div>
  );
}
