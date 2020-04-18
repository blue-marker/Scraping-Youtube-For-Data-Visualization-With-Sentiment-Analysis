import nltk
import random
from nltk.corpus import movie_reviews
from nltk import word_tokenize
from nltk.classify import ClassifierI
from statistics import mode
import pickle

def find_features(listOfwords):
    words = word_tokenize(listOfwords)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features





class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes =[]
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

short_pos = open("positive.txt","r").read()
short_neg = open("negative.txt","r").read()

all_words =[]
documents = []

# j i adject, r is adverb, and v is verb
#allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]

for p in short_pos.split('\n'):
    documents.append((p,"pos"))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

for n in short_neg.split('\n'):
    documents.append((n,"neg"))
    words = word_tokenize(n)
    neg = nltk.pos_tag(words)
    for w in neg:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

# for r in short_pos.split('\n'):
#     documents.append((r,"pos"))
#
# for r in short_neg.split('\n'):
#     documents.append((r,"neg"))

# print(documents[0])
# documents = [(list(movie_reviews.words(fileid)),category)
#             for category in movie_reviews.categories()
#             for fileid in movie_reviews.fileids(category)]
# print(documents[1])
# print(type(documents))
# random.shuffle(documents)
# for category in movie_reviews.categories():
#     print(category)
#     for fileid in movie_reviews.fileids(category):
#         print(fileid)
#         documents.append((list(movie_reviews.words(fileid)),category))

# all_words = []
# for w in movie_reviews.words():
#     all_words.append(w.lower())
#
# all_words = nltk.FreqDist(all_words)
# print(type(all_words))
# print(all_words.most_common(15))
#
# print(all_words["awesome"])
# print(documents[1])

# short_pos_words = word_tokenize(short_pos)
# short_neg_words = word_tokenize(short_neg)
#
# for w in short_pos_words:
#     all_words.append(w.lower())
#
# for w in short_neg_words:
#     all_words.append(w.lower())

# print(all_words)
all_words= nltk.FreqDist(all_words)
# print(all_words[9])

word_features = list(all_words.keys())[:5000]



# print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

featuresets = [(find_features(rev), category) for (rev, category) in documents]

random.shuffle(featuresets)

# print(featuresets[2])
# print(featuresets[8])
# print(featuresets[9])

training_set = featuresets[:10000]
testing_set = featuresets[10000:]


# classifier = nltk.NaiveBayesClassifier.train(training_set)

classifier_f = open("naivebayes.pickle",'rb')
classifier = pickle.load(classifier_f)
classifier_f.close()

print("Naive Bayes Algo accuracy percent:",(nltk.classify.accuracy(classifier,testing_set))*100)
# classifier.show_most_informative_features(15)

# save_classifier = open("naivebayes.pickle",'wb')
# pickle.dump(classifier,save_classifier)
# save_classifier.close()

# def sentiment(text):
#     pasta = find_features(text)
#     classifier
#     return pasta


voted_classifier = VoteClassifier(classifier)

# print(voted_classifier.classify(['This','was','horrible','.','I','was','really','bad','.','worse']))
# print(classifier("This was a really good movie"))

def sentiment(text):
    feats= find_features(text)

    return voted_classifier.classify(feats)


# print(sentiment("This movie was awesome ! The acting was great, plot was wonderful."))
# print(sentiment("This movie was utter junk. There were absolutely no pythons.Honestly a waste of time."))



