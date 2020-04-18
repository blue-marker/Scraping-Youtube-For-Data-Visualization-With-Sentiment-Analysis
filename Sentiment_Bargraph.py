import csv
import numpy as np
from matplotlib import pyplot as plt

#Textblob is built on NLTK tool
#which is again used for sentiment analysis
from textblob import TextBlob

k=0

class Sentiment_Bargraph:

    def __init__(self):
        global k
        plt.style.use("fivethirtyeight")

        comments= open('comments.csv',encoding='utf')

        reader = csv.DictReader(comments)

        next(reader)
        poslist = []
        neglist = []
        # neulist = []
        pos = 0
        neg = 0
        # neu = 0
        idlist=[]

        for i,row in enumerate(reader):

            if row['Video ID'] not in idlist:

                idlist.append(row['Video ID'])

                poslist.append(pos)
                neglist.append(neg)
                # neulist.append(neu)
                pos = 0
                neg = 0
                # neu = 0

            # k = sentiment(row['Comment'])

            analysis = TextBlob(row['Comment'])
            emo = float(float((analysis.sentiment.polarity)) * 100)

            if emo > 0:
                k = 'pos'
            elif emo < 0:
                k = 'neg'
            # else:
            #     k = 'neu'

            if k == 'pos':
                pos += 1
                # print(pos)
            elif k == 'neg':
                neg += 1
                # print(neg)
            # elif k == 'neu':
            #     neu += 1

        poslist.append(pos)
        neglist.append(neg)
        # neulist.append(neu)
        poslist.remove(0)
        neglist.remove(0)
        # neulist.remove(0)
        # print(idlist)
        # print(len(idlist))


        xlist=[]
        with open('Channel_Names.csv','r') as y:
            # fieldnames=('Channel Name')
            reader = csv.DictReader(y)

            for row in reader:

                xlist.append(row['Channel Name'])
        # print(xlist)

        x_indixes = np.arange(len(idlist))
        width = 0.20
        # print(poslist)
        # print(neglist)
        plt.bar(x_indixes - width,poslist,width =width,color="#008fd5", label = 'Positive comments')
        # plt.bar(x_indixes , neulist, width=width, color="#e5ae38", label='Neutral comments')
        plt.bar(x_indixes ,neglist,width =width,color="tomato", label = 'Negative comments')

        plt.legend()

        plt.xticks(ticks=x_indixes, labels=xlist,rotation=90)
        plt.title("Sentiment Analysis")
        plt.xlabel('Channel Names')
        plt.ylabel('No Of Comments')
        plt.tight_layout()
        plt.show()

