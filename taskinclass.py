import sys
import requests
 
CLIENT_ID = "paste your client id here"
CLIENT_SECRET = "paste your secret here"
USERNAME = "your_reddit_username"
HEADERS = {"User-Agent": "python:subreddit-info:v1.0 (by /u/" + USERNAME + ")"}
 
name = sys.argv[1] if len(sys.argv) > 1 else "learnpython"
 
#  log in to get a token
login = requests.post("https://www.reddit.com/api/v1/access_token",
                      auth=(CLIENT_ID, CLIENT_SECRET),
                      data={"grant_type": "client_credentials"},
                      headers=HEADERS)
if "access_token" not in login.json():
    sys.exit("Login failed. Check your keys.")
HEADERS["Authorization"] = "bearer " + login.json()["access_token"]
 
 
#  a helper that asks Reddit for data
def ask(path, **options):
    r = requests.get("https://oauth.reddit.com" + path, params=options, headers=HEADERS)
    if r.status_code != 200:
        sys.exit("Reddit error " + str(r.status_code) + " (wrong name or private?)")
    return r.json()
 
 
info = ask("/r/" + name + "/about")["data"]
rules = ask("/r/" + name + "/about/rules")["rules"]
post = ask("/r/" + name + "/top", t="all", limit=1)["data"]["children"][0]["data"]
 
#  print the results
print("Community:   r/" + info["display_name"])
print("Subscribers: " + format(info["subscribers"], ","))
print("Description: " + info["public_description"])
print("Rules:")
for number, rule in enumerate(rules, 1):
    print("  " + str(number) + ". " + rule["short_name"])
print("Top post:    " + post["title"])
print("Upvotes:     " + format(post["score"], ","))
print("Link:        https://www.reddit.com" + post["permalink"])
 
