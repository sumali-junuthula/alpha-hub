import React from "react";

export default function RedditFeed({ posts }) {
  if (!posts || posts.length === 0) {
    return <p className="text-center text-gray-400">No Reddit posts found.</p>;
  }

  return (
    <div className="bg-zinc-900 rounded-xl p-6 mt-6 shadow-lg ring-1 ring-zinc-700">
      <h2 className="text-xl font-bold text-white mb-4">🧠 Reddit Sentiment</h2>
      <div className="space-y-4">
        {posts.map((post, idx) => (
          <a
            key={idx}
            href={post.url}
            target="_blank"
            rel="noopener noreferrer"
            className="block bg-zinc-800 hover:bg-zinc-700 transition rounded-lg p-4 border border-zinc-700"
          >
            <h3 className="text-white font-semibold">{post.title}</h3>
            <p className="text-sm text-gray-400 mt-1">👍 {post.upvotes} | 💬 {post.comments}</p>
          </a>
        ))}
      </div>
    </div>
  );
}
