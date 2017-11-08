# import libraries to work with mongoDB
import requests
from pymongo import MongoClient

# import text processing libraries
import string
import re

# import natural language processing toolkit libraries
import nltk.classify.util
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.collocations import *

# import data visualisation libraries
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Collection lookup list
# "Fushimi_Inari_Shrine",
# "Hiroshima_Peace_Memorial_Park",
# "Jigokudani_Snow_Monkey_Park",
# "Kiyomizu_Dera",
# "Tokyo_Disneyland"

# define the attraction collection intended for analysis according to lookup list
attraction = "Hiroshima_Peace_Memorial_Park"

# Initialization of MongoDb server
client = MongoClient("localhost", 27017)
db = client.tripAdvisor
collection = db['comments_at_'+ attraction]

# check the number of documents available in the collection(one document represents one review comment)
print("number of documents inserted :", collection.count())

# check the review rating distribution
print("number of documents inserted (Rating = 1) :", collection.find({"Rating": "1"}).count())
print("number of documents inserted (Rating = 2) :", collection.find({"Rating": "2"}).count())
print("number of documents inserted (Rating = 3) :", collection.find({"Rating": "3"}).count())
print("number of documents inserted (Rating = 4) :", collection.find({"Rating": "4"}).count())
print("number of documents inserted (Rating = 5) :", collection.find({"Rating": "5"}).count())

# Concatenate all the reviews into one huge text file
text_list=""
for x in collection.find({}):
    text_list += " " + x['Comment']

# Change all the word in text list into lower case for normalization
text_list = text_list.lower()

# remove all the not english word or weird word in the text list
printable = set(string.printable)
text_list = ''.join(filter(lambda x: x in printable, text_list))

# remove all the punctuation in the text list and store in a word list
tokenizer = RegexpTokenizer(r'\w+')
words = tokenizer.tokenize(text_list)

# remove all the english stopwords in the word list
meaningful_words = [word for word in words if word not in stopwords.words('english')]

# tag each of the word in the text list with their grammatically word class
meaningful_words_tag = nltk.pos_tag(meaningful_words)

# create a new word list from the original word list with only adjective
meaningful_words_adjective = []
for word, tag in meaningful_words_tag:
    if tag.startswith('JJ'):
        meaningful_words_adjective.append(word)

# create a new word list from the original word list with only noun
meaningful_words_noun = []
for word, tag in meaningful_words_tag:
    if tag.startswith('NN'):
        meaningful_words_noun.append(word)

# create a new word list from the original word list with only verb
meaningful_words_verb = []
for word, tag in meaningful_words_tag:
    if tag.startswith('VB'):
        meaningful_words_verb.append(word)

# extract the frequency of each word in each of the word list
freq_dist_noun = nltk.FreqDist(meaningful_words_noun)
freq_dist_adjective = nltk.FreqDist(meaningful_words_adjective)
freq_dist_verb = nltk.FreqDist(meaningful_words_verb)

# show the top 10 common adjective
freq_dist_adjective.most_common(10)

# show the top 10 common noun
freq_dist_noun.most_common(10)

# show the top 10 common verb
freq_dist_verb.most_common(10)

# join each of the word list into a string
meaningful_words_string = ' '.join(word for word in meaningful_words)
meaningful_words_adjective_string = ' '.join(word for word in meaningful_words_adjective)
meaningful_words_noun_string = ' '.join(word for word in meaningful_words_noun)
meaningful_words_verb_string = ' '.join(word for word in meaningful_words_verb)

# Generate a all word cloud image
wordcloud = WordCloud().generate(meaningful_words_string)
plt.figure(figsize=(10, 8))
plt.title(attraction +' Overall Word Cloud', fontsize = 20)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# Generate a adjective word cloud image
wordcloud = WordCloud().generate(meaningful_words_adjective_string)
plt.figure(figsize=(10, 8))
plt.title(attraction +' Adjective Word Cloud', fontsize = 20)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# Generate a noun word cloud image
wordcloud = WordCloud().generate(meaningful_words_noun_string)
plt.figure(figsize=(10, 8))
plt.title(attraction +' Noun Word Cloud', fontsize = 20)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# Generate a verb word cloud image 
wordcloud = WordCloud().generate(meaningful_words_verb_string)
plt.figure(figsize=(10, 8))
plt.title(attraction +' Verb Word Cloud', fontsize = 20)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

### Generate top 10 double words phrase
print("Top 10 double words phrase")
bigram_measures = nltk.collocations.BigramAssocMeasures()
finderb = BigramCollocationFinder.from_words(words)
#ignore bigrams which occur less than three times
finderb.apply_freq_filter(3)
#Top 10 bigram collocations
for i in (finderb.nbest(bigram_measures.pmi, 10)):
    print (i)

### Generate top 10 double words phrase or 5 stars rating
# Concatenate all the reviews into one huge text file

print("---Top 10 double words phrase or 5 stars rating---")
text_list=""
for x in collection.find({"Rating":"5"}):
    text_list += " " + x['Comment']

# Chnage all the text into lower case for normalization
text_list = text_list.lower()

# remove all the not english word or weird word
printable = set(string.printable)
text_list = ''.join(filter(lambda x: x in printable, text_list))

# remove all the punctuation
tokenizer = RegexpTokenizer(r'\w+')
words = tokenizer.tokenize(text_list)

# remove all the english stopwords 
meaningful_words = [word for word in words if word not in stopwords.words('english')]

bigram_measures = nltk.collocations.BigramAssocMeasures()
finderb = BigramCollocationFinder.from_words(words)
#ignore bigrams which occur less than three times
finderb.apply_freq_filter(3)
#Top 10 bigram collocations
for i in (finderb.nbest(bigram_measures.pmi, 10)):
    print(i)
