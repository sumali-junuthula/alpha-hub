import os
import praw
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
  client_id=os.getenv("REDDIT_CLIENT_ID"),
  client_secret=os.getenv("REDDIT_SECRET"),
  user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_reddit_posts(ticker: str, limit: int = 10):
  subreddit = reddit.subreddit("stocks")
  query = ticker
  posts = subreddit.search(query, sort="new", limit=limit)

  results = []
  for post in posts:
    results.append({
      "title": post.title,
      "url": post.url,
      "score": post.score,
      "created_utc": post.created_utc,
      "num_comments": post.num_comments
    })

  return results
