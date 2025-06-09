import os
import praw
from dotenv import load_dotenv
from config import REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT, REDDIT_USERNAME, REDDIT_PASSWORD

load_dotenv()

reddit = praw.Reddit(
  client_id=REDDIT_CLIENT_ID,
  client_secret=REDDIT_SECRET,
  user_agent=REDDIT_USER_AGENT,
  usename=REDDIT_USERNAME,
  password=REDDIT_PASSWORD
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
