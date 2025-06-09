import React from "react";
import { motion } from "framer-motion";

export default function RedditFeed({ posts }) {
  if (!posts || posts.length === 0) {
    return (
      <p className="text-center text-gray-400 mt-6">
        No Reddit posts found.
      </p>
    );
  }

  return (
    <div className="mt-14">
      {/* Section Header */}
      <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-sky-300 via-cyan-300 to-blue-200 drop-shadow-lg mb-6 tracking-tight">
        🧠 Reddit Sentiment
      </h2>

      {/* Horizontal Scrollable Carousel */}
      <div className="relative overflow-x-auto snap-x snap-mandatory flex gap-6 px-4 pb-2 scroll-smooth scrollbar-thin scrollbar-thumb-zinc-700">
        {posts.slice(0, 10).map((post, idx) => (
          <motion.a
            key={idx}
            href={post.url}
            target="_blank"
            rel="noopener noreferrer"
            className="snap-center bg-zinc-900 border border-blue-500/30 hover:border-blue-400 transition rounded-2xl p-6 text-white min-w-[80%] md:min-w-[60%] lg:min-w-[40%] cursor-pointer shadow-md"
            whileHover={{
              scale: 1.02,
              boxShadow: "0 0 20px rgba(59,130,246,0.25)",
            }}
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: idx * 0.1 }}
            viewport={{ once: true }}
          >
            <div className="text-sm text-blue-400 mb-1">
              #{idx + 1} of {posts.length}
            </div>
            <h3 className="text-lg font-bold text-blue-300 mb-2">
              {post.title}
            </h3>
            <p className="text-zinc-400 text-sm mt-2 line-clamp-3">
              👍 {post.upvotes} | 💬 {post.comments}
            </p>
          </motion.a>
        ))}
      </div>
    </div>
  );
}
