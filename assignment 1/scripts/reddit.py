import praw
import csv
import time

# Reddit API credentials
reddit = praw.Reddit(client_id="your_client_id",
                     client_secret="your_client_secret",
                     user_agent="your_user_agent")

def fetch_reddit_data(subreddit_name, keyword, limit=100):
    
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    
    for post in subreddit.search(keyword, limit=limit):
        posts.append([
            post.title,
            post.selftext,
            post.author.name if post.author else "N/A",
            post.created_utc,
            post.score,
            subreddit_name
        ])
        time.sleep(1)  

    return posts

def save_to_csv(data, filename):

    headers = ["title", "text", "author", "date", "upvotes", "subreddit"]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

subreddits = ["ElectricVehicles", "TeslaMotors"]
all_posts = []

for sub in subreddits:
    all_posts.extend(fetch_reddit_data(sub, "electric vehicle"))

save_to_csv(all_posts, "datasets/raw/reddit_posts.csv")

print("Reddit data saved.")
