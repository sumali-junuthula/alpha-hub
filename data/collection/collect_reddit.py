import os
import praw
import pandas as pd
from dotenv import load_dotenv
from config import REDDIT_KEYWORD, REDDIT_SUBREDDIT, REDDIT_LIMIT

load_dotenv()
reddit = praw.Reddit(
  client_id=os.getenv("REDDIT_CLIENT_ID"),
  client_secret=os.getenv("REDDIT_SECRET"),
  user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_reddit(keyword=REDDIT_KEYWORD, subreddit=REDDIT_SUBREDDIT, limit=REDDIT_LIMIT):
  posts = reddit.subreddit(subreddit).search(keyword, sort="new", limit=limit)
  rows = []
  for post in posts:
    rows.append({
      "title": post.title,
      "score": post.score,
      "created_utc": post.created_utc,
      "num_comments": post.num_comments,
      "url": post.url
    })
  
  df = pd.DataFrame(rows)
  df.to_csv("data/output/reddit.csv", index=False)
  print(f"Saved {len(df)} Reddit posts to data/output/reddit.csv")

if __name__ == "__main__":
  fetch_reddit()
