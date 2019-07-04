import json
import requests
import argparse
from time import sleep
from InstagramAPI import InstagramAPI
import os, os.path

# Functions
def mpath(fpath):
	return os.path.join(os.getcwd(), fpath)


# Arugments

"""parser = argparse.ArgumentParser(description='Like X posts every Y minutes from hashtag')
parser.add_argument('hashtag', metavar='H', type=str, help='The hashtag that will be scraped')
parser.add_argument('post_count', metavar='X', type=int, help='The number of posts, X, that will be liked every Y minutes')
parser.add_argument('interval', metavar='Y', type=int, help='The interval, the every amount of minutes, Y, X posts will be liked')
parser.add_argument('username', metavar='U', type=str, help='The username of the account that will like the posts')
parser.add_argument('password', metavar='P', type=str, help='The password of the account that will like the posts')

args = parser.parse_args()"""


# Data grabbing

def jdump(fname, data_dict):
	with open(fname, 'w', encoding='utf-8') as f:
		json.dump(data_dict, f, indent=4)

def get_ig_page(url, session=None):
	#print(url)
	#session = session or requests.Session()
	r = requests.get(url)
	r_code = r.status_code

	if r_code == 200:
		# The code is 200 or valid
		return r
	else:
		return None

def get_media_ids():
	while True:
		ig_data_dict = get_ig_page(url)

		if ig_data_dict is not None:
			ig_data_dict = ig_data_dict.json()
			#jdump(mpath('posts.json'), ig_data_dict)
			#print("Retrieving media ids from url", url)
		else:
			print("Oops something went wrong")


		try:
			media_ids = [m['node']['id'] for m in ig_data_dict['graphql']['hashtag']['edge_hashtag_to_media']['edges']]
			break
		except:
			print ("ALERT: API RETURNED A NONE TYPE, RELOADING API AFTER 2 MINUTES")
			sleep(120)
	return media_ids

# config
def examineConfig(data):
	assert data['interval'].strip().isdigit(), "interval must be numbers only, decimals and letters are not accepted"
	assert data['post_count'].strip().isdigit(), "interval must be numbers only, decimals and letters are not accepted"
	assert len(data['hashtag'].strip()) > 0, "subreddit cannot be empty"
	assert len(data['instagram_username'].strip()) > 0, "instagram username cannot be empty"
	assert len(data['instagram_password'].strip()) >= 8, "instagram_password cannot be less than 8 characters"

def loadConfig():
	try:
		with open(mpath('config.json'), 'r') as f:
			data = json.load(f)
			examineConfig(data)
			print("config.json loaded successfully!")

	except FileNotFoundError:
		print("config.json not found, creating new settings file.")

		with open(mpath('config.json'), 'w') as f:
			data = {'hashtag':'ADD YOUR PREFERRED HASHTAG',
					'post_count': 'THE NUMBER OF POSTS, X, THAT WILL BE LIKED EVERY Y MINUTES',
					'interval': 'THE INTERVAL, THE EVERY AMOUNT OF MINUTES, Y, X POSTS WILL BE LIKED',
					'instagram_username': 'ADD YOUR INSTAGRAM USERNAME HERE',
					'instagram_password': 'ADD YOUR INSTAGRAM PASSWORD HERE',
					}
			json.dump(data, f, indent=4)

		print("config.json successfully created, please edit config.json with correct configuration and run the script again")

		exit(1)

	return (data['hashtag'].strip(), int(data['post_count'].strip()), 
		int(data['interval'].strip()), data['instagram_username'].strip(), data['instagram_password'].strip())

# json

def SetupJson():
	try:
		with open(mpath('posted.json'), 'r', encoding='utf8') as f:
			pass
	except FileNotFoundError:
		with open(mpath('posted.json'), 'w', encoding='utf-8') as f:
			data = {'posted':[]}
			json.dump(data, f, indent=4)

def AddPostToPosted(postlink):
	with open(mpath('posted.json'), 'r+', encoding='utf-8') as f:
		data = json.load(f)
		data['posted'].append(postlink)
		f.seek(0)
		f.truncate()
		json.dump(data, f, indent=4)

def CheckIfPosted(postlink):
	try:
		with open(mpath('posted.json'), 'r', encoding='utf-8') as f:
			data = json.load(f)
			if postlink in data['posted']:
				#
				return True
			else:
				#
				return False
	except:
		print("error in CheckIfPosted")

# load config
hashtag, post_count, interval, instagram_username, instagram_password = loadConfig()

# Application
accum = 0
url = f"https://www.instagram.com/explore/tags/{hashtag}/?__a=1"
media_ids = get_media_ids(url)
SetupJson()
picposted = False

# login to instagram
print ("logging in to instagram")
insta_api = InstagramAPI(instagram_username, instagram_password)
if (insta_api.login()):
	print ("login successful")
else:
	print ("ERROR: Failed to login to Instagram, please make sure you've used the correct username and password and that the connection is not faulty as well.")
	exit(1)

while True:
	for i in range(post_count):
		if accum >= len(media_ids):
			#print (len(media_ids))
			accum = 0
			sleep(interval * 60)
			media_ids = get_media_ids(url)
			break
		if not CheckIfPosted(media_ids[accum]):
			insta_api.like(media_ids[accum])
			AddPostToPosted(media_ids[accum])
			picposted = True
			print("liked photo with media id", media_ids[accum])
		#else:
			# print("photo with media id", media_ids[accum], "already liked. skipping")
		accum += 1
	else:
		continue

	if not picposted:
		print ("the photos in the current loop are all liked.")
	picposted = False
	sleep(interval * 60)
	print(f"Sleeping for {interval} minutes")