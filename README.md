# instagram-tag-liker
A bot that likes instagram posts on time intervals.


**First of all, download the repository and open a command prompt at the path of the repository Make sure you're using Python 3, atleast version >= 3.72**

# Install the dependencies
`pip install -r requirements.txt` Depending on your OS, you may have to use `pip3` instead.

# Setup Configuration File.
⋅## ⋅1. Run the script (You'll get an error, but 2 new files — config.json and app.log— will appear)

You can run the script using python script.py. Depending on your OS, you might have to use python3 instead. You'll see this when you run the script

```
Log Setted Up
config.json not found, creating new settings file.
config.json successfully created, please edit config.json with correct configuration and run the script again
```

## ⋅⋅2. Open and edit config.json
You should see this
```
{
    "hashtag": "ADD YOUR PREFERRED HASHTAG",
    "post_count": "THE NUMBER OF POSTS, X, THAT WILL BE LIKED EVERY Y MINUTES",
    "interval": "THE INTERVAL, THE EVERY AMOUNT OF MINUTES, Y, X POSTS WILL BE LIKED",
    "instagram_username": "ADD YOUR INSTAGRAM USERNAME HERE",
    "instagram_password": "ADD YOUR INSTAGRAM PASSWORD HERE"
}
```
* _hashtag_ is the hashtag, without the #
* _post_count_ is the number of posts that will be liked, from the hashtag, every Y minutes.
* _interval_ is the interval, in minutes. Every Y minutes, X posts will be liked from the hashtag. INTEGER VALUES ONLY
* _instagram_username_ is the username of the instagram account that will like the posts
* _instagram_password_ is the password of the instagram account that will like the posts

save config.json after you're done

## 3. Run the script.
The script should run fine then. a new files will show up, ```posted.json```


<sub><sup><a href="https://www.youtube.com/watch?v=jypU9mjeJqw">Some code was borowwed from here</a></sup></sub>
