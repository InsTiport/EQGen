# EQGen

## Scraping Reddit
To scrape all submissions(posts) from a subreddit, use `reddit_scraper.py` under the `scraping` folder. To use this script, you need to [set up credentials](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#prerequisites) and put those into a file called `reddit_credentials.txt` under the `scraping` folder. Inside the file, put client ID, client secret and user agent in three separate lines (in this specific order).

The default behavir, i.e. running it without any arguments, is to scape all posts from [r/socialskills](https://www.reddit.com/r/socialskills/). To scrape other subreddits, use

```python
python reddit_scraper.py -s [name of subreddit]
```
