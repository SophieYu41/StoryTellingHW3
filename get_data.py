from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json, redis

# variables that contains the user credentials to access Twitter API 
access_token = "2843768163-8lapJ7O50xPWxkmAwWIhi8kgaOrflPgmG1xQC9W"
access_token_secret = "gaNrKB1BUN1fSX10U7NAtPKv65WwHfbrH8dlQ5j4LxVxf"
consumer_key = "NUCwbIkKkd20W8iHIYoOxlv0b"
consumer_secret = "6P2uOCOb0Xb8ZLkQ17PRTRl05T0BFC9EaToDB5sLSnI1TQONGU"

# set up redis connections
pool_trump = redis.ConnectionPool(host='localhost', port=6379, db=0)
pool_clinton = redis.ConnectionPool(host='localhost', port=6379, db=1)
conn_trump = redis.Redis(connection_pool=pool_trump)
conn_clinton = redis.Redis(connection_pool=pool_clinton)

# this is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        add_tweet(data)
        return True


# add tweet to redis database
def add_tweet(data):
	try:
		# decode json string from the result
		obj = json.loads(data)
		time = obj['created_at']
		#print time
		text = obj['text']
		if 'donaldtrump' in text.lower():
			conn_trump.setex(time, 'trump', 60)
			print 'add tweet for trump'
		if 'hillaryclinton' in text.lower():
			conn_clinton.setex(time, 'clinton', 60)
			print 'add tweet for clinton'
	except ValueError:
		print e.errno


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords and locations
    stream.filter(track=['hillaryclinton', 'donaldtrump'])