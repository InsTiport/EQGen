import os
import json
import praw
import tqdm
import argparse
from psaw import PushshiftAPI


def make_tree(comment):
    tree = {'body': comment.body, 'author': str(comment.author), 'ups': comment.ups}

    if len(comment._replies) > 0:
        tree['replies'] = []
        for reply in comment._replies:
            tree['replies'].append(make_tree(reply))

    return tree


'''
General setup
'''
# setup args
arg_parser = argparse.ArgumentParser()

arg_parser.add_argument(
    '-s', '--subreddit',
    type=str,
    default='socialskills',
    help='Specify the subreddit you want to scrape'
)

args = arg_parser.parse_args()
os.chdir('../')

'''
Find all posts under a user specified subreddit
'''
api = PushshiftAPI()

gen = api.search_submissions(subreddit=args.subreddit)

counter = 0
posts = []
for result in gen:
    if result.author != '[deleted]':
        try:
            posts.append((result.title, result.author, result.selftext, result.full_link))
        except AttributeError:
            posts.append((result.title, result.author, '', result.full_link))
        counter += 1

print(f'There are {counter} submissions in total under r/{args.subreddit}. Start scraping individual posts.')

'''
Scraping individual posts
'''
try:
    with open(os.path.join('scraping', 'reddit_credentials.txt')) as r:
        lines = r.readlines()
        client_id, client_secret, user_agent = [line.strip() for line in lines]
except FileNotFoundError:
    print('Please add the credential file under scraping folder.')
    print('See https://praw.readthedocs.io/en/stable/getting_started/quick_start.html#prerequisites for details.')
    print('While creating this file, put client ID, client secret and user agent in 3 separate lines (in this order).')
    exit(0)

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

os.makedirs(os.path.dirname('data' + '/'), exist_ok=True)
os.makedirs(os.path.dirname(os.path.join('data', args.subreddit) + '/'), exist_ok=True)
for title, author, self_text, link in tqdm.tqdm(posts):
    submission = reddit.submission(url=link)

    submissionTree = []

    for top_level_comment in submission.comments:
        submissionTree.append(make_tree(top_level_comment))

    js = json.dumps(submissionTree)
    with open(os.path.join('data', args.subreddit, title.replace(' ', '_').replace('/', '><')), 'w') as w:
        w.write(f'{title}\n')
        w.write(f'{author}\n')
        w.write(f'{self_text}\n')
        w.write(f'{js}\n')
        w.write(f'{link}\n')
