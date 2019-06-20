import json
import requests
import argparse
from time import sleep
from InstagramAPI import InstagramAPI

# Functions
def mpath(fpath):
	return os.path.join(os.getcwd(), fpath)


# Arugments

parser = argparse.ArgumentParser(description='Like X posts every Y minutes from hashtag')
parser.add_argument('hashtag', metavar='H', type=str, help='The hashtag that will be scraped')
parser.add_argument('post_count', metavar='X', type=int, help='The number of posts, X, that will be liked every Y minutes')
parser.add_argument('interval', metavar='Y', type=int, help='The interval, the every amount of minutes, Y, X posts will be liked')
parser.add_argument('username', metavar='U', type=str, help='The username of the account that will like the posts')
parser.add_argument('password', metavar='P', type=str, help='The password of the account that will like the posts')

args = parser.parse_args()

url = f"https://www.instagram.com/explore/tags/{args.hashtag}/?__a=1"


# Data grabbing

def jdump(fname, data_dict):
	with open(fname, 'w', encoding='utf-8') as f:
		json.dump(data_dict, f, indent=4)

def get_ig_page(url, session=None):
	print(url)
	session = session or requests.Session()
	r = session.get(url)
	r_code = r.status_code

	if r_code == 200:
		# The code is 200 or valid
		return r
	else:
		return None


def get_media_ids(url):
	ig_data_dict = get_ig_page(url)

	if ig_data_dict is not None:
		ig_data_dict = ig_data_dict.json()
		#jdump(mpath('posts.json'), ig_data_dict)
		print("Retrieving media ids from url", url)
	else:
		print("Oops something went wrong")

	media_ids = [m['node']['id'] for m in ig_data_dict['graphql']['hashtag']['edge_hashtag_to_media']['edges']]
	return media_ids

# login to instagram
print ("logging in to instagram")
insta_api = InstagramAPI(args.username, args.password)
if (insta_api.login()):
	print ("login successful")
else:
	print ("ERROR: Failed to login to Instagram, please make sure you've used the correct username and password and that the connection is not faulty as well.")
	exit(1)

# Application
accum = 0
media_ids = get_media_ids(url)

while True:
	for i in range(args.post_count):
		if accum >= len(media_ids):
			accum = 0
			media_ids = get_media_ids(url)
			break

		insta_api.like(media_ids[accum])
		accum += 1
		print("liked photo with media id", media_ids[accum])

	sleep(args.interval * 60)
	print(f"Sleeping for {args.interval} minutes")