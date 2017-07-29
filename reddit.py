import requests
import requests.auth

import json
from collections import namedtuple

import reddit_keys as rk
import reddit_posts as posts

import time
import sys

#### USAGE ###
# python reddit.py
# looks for a post from the current hour. if one exists, post it.

#TODO implement 10 minute interval for xposting

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

client_auth = requests.auth.HTTPBasicAuth(rk.app_key, rk.app_private)
post_data = {"grant_type": "password", "username": rk.auth_user, "password": rk.auth_pass}
headers = {"User-Agent": "SubmitClient/0.1 by testbot"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

access_token = response.json()['access_token']

filename = "./reddit_log.txt"

datestr = time.strftime("%Y_%m_%d_%H")


try:
	mypost = eval("posts.post_"+datestr)
	headers = {"Authorization": "bearer " + access_token, "User-Agent": "SubmitClient/0.1 by testbot"}
	post_data = {"sr":mypost["sr"],"kind":"link","sendreplies":"true","title":mypost["title"],"url":mypost["url"]}
	response = requests.post("https://oauth.reddit.com/api/submit", data=post_data, headers=headers)

	with open(filename, "a") as myfile:
		myfile.write(datestr+"\n"+str(response.json())+"\n")
except AttributeError:
	with open(filename, "a") as myfile:
		myfile.write("nothing found at "+datestr+"\n")
except:
	with open(filename, "a") as myfile:
		myfile.write("Unexpected error: "+sys.exc_info()[0])




#### GET FLAIR
# headers = {"Authorization": "bearer " + access_token, "User-Agent": "SubmitClient/0.1 by testbot"}
# response = requests.get("https://oauth.reddit.com/r/smashbros/api/link_flair", headers=headers);
# print response.json()