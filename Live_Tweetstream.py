#To get live tweets from Twitter API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#To clean the tweets
import json
import re

#For applying sentiment analysis on tweets
from textblob import TextBlob
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation




posinegiTweet=[]
x_value=[]
j=0



class listener(StreamListener):

    def on_data(self, data):

        all_data= json.loads(data)
        test = all_data['text']
        # print(all_data['text'])
        # ata= ''.join(re.sub('[RT\s@][A-Za-z].', '', test))
        tweet_text = ''.join(re.sub('(http://|https://){1}[A-Za-z]+\.[a-z.A-Z{3}][.a-zA-Z]*', '', test))

        print(tweet_text)
        analysis = TextBlob(tweet_text)
        emo = float(float((analysis.sentiment.polarity))*100)
        output = open('tweets.csv','a')
        output.write(str(emo))
        output.write('\n')
        output.close()
        # print(emo)

        if emo > 0:
            print('pos',emo)
            posinegiTweet.append(int(emo))
            x_value.append(j)
        elif emo < 0:
            print('neg', emo)
            posinegiTweet.append(int(emo))
            x_value.append(j)
        else:
            print('neu', emo)
            posinegiTweet.append(int(emo))
            x_value.append(j)

        return(True)


    def on_error(self, status):
        print(status)


#For getting live stream of tweets
class Tweetstream:
    # consumer key, consumer secret, access token, access secret.

    ckey = 'Y0nYB0zDpF2UXE3m8tqYESmlH'
    csecret = 'hjfWWSlNMNv7yPcq6J9LqzecRvTuS2ehQwRD3HSE8SrucgZRrA'
    atoken = '824426210-ErWlVCHNTfYDJVpjqtwmlaGzEUffgIJhw7IWm9vZ'
    asecret = 'QbWRmC5utm5jiDBYNEmgWk7j49ah31YHUR0kZrPA0Yzwe'


    def twitty(self,tweek):
        auth = OAuthHandler(self.ckey, self.csecret)
        auth.set_access_token(self.atoken, self.asecret)

        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=[tweek])

#For generating Live Graph
class Tweetgraph:

    def animate(self,i):
        # global j
        # j +=1
        pullData= open('tweets.csv','r').read()
        lines = pullData.split('\n')

        xar=[]
        yar=[]

        x=0
        y=0

        for l in lines:
            # print(type(l))
            # print(float(l))
            x += 1
            if '-' not in l:
                y +=1
            elif '-' in l:
                y -=1

            xar.append(x)
            yar.append(y)

        plt.cla()
        plt.plot(xar,yar)


    def livegraph(self):
        plt.style.use('fivethirtyeight')

        ani = FuncAnimation(plt.gcf(), self.animate, interval=1000)
        plt.tight_layout()
        plt.show()
