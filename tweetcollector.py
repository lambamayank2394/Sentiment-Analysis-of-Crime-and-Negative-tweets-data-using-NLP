from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests

consumer_key = 'NScfytb3inyC26M5JrA7RLrbU'
consumer_secret = 'ZuKVVJh80NN0W0vjmXA9Vmpp2RgTjlo372nZpIGg4ZVY0Xpcyj'
access_token = '916904578490171392-rHr23i95aSfeQjnBmunr3dtHofvGeV4'
access_secret = 'pZwQCTdnVpYAiZWo2u5ixLscm1N1vheuxX42OVIEdcUp0'

class StdOutListener(StreamListener):

    def on_data(self, data):
        data_json = json.loads(data)
        try:
            # fetch tweets coordinates
            coordinates = data_json['place']['bounding_box']['coordinates']
            # fetch tweets text
            tweet = data_json['text']
            place = data_json['place']

            if place is not None:       # if place is not empty
                if coordinates[0] is not None and len(coordinates[0]) > 0:           # And coordinates are known
                    avg_x = 0
                    avg_y = 0
                    for c in coordinates[0]:
                        # avg of x cal
                        avg_x = (avg_x + c[0])
                        # avg of y cal
                        avg_y = (avg_y + c[1])
                    avg_x /= len(coordinates[0])
                    avg_y /= len(coordinates[0])
                    coordinates = [avg_x, avg_y]      # Calculating coordinates value
                final_data = {                          # final data with tweets and coordinates
                    "tweet": tweet,
                    "coordinates": coordinates
                }
                print(final_data)
                # requests.post(host_name,json=final_data)      # pushing to elastic search with hostname specified in file credentials
        except (KeyError, TypeError):
            pass
        return True

    def on_error(self, status):
        #print status on error
        print (status)

if __name__ == '__main__':
    # Twitter Api Keys from credentials file
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    # Calling StdOutListener function
    stream = Stream(auth, StdOutListener())
    # Filter the stream through mentioned keywords
    stream.filter(
        track=['trump', 'federer', 'nyu', 'new york', '#ind', 'location', 'amazon', 'hugh', 'pizza', 'snapchat',
               'instagram', 'facebook', 'bitcoin', 'violets', 'messi', 'ronaldo', 'money', 'dan brown', 'apple',
               'iphone X','iphone8', 'Google home mini', 'Googe', 'Apple watch', 'Macbook', 'iphone', 'Trending', 'Me too',
               'Alexa','elections', 'Chelsea', 'Man United', 'Nadal', 'ATP', 'ATP tour', 'BCCI', 'NASA', 'ISRO', 'SRK', 'KRK'])
