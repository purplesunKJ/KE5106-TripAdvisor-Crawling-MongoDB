# import libraries to work with mongoDB
import requests
from pymongo import MongoClient

# import text processing libraries
import pandas as pd
import string
import re

# import natural language processing toolkit libraries, if have not downloaded, can run the download syntax
import nltk
#nltk.download()
import nltk.classify.util
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

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
attraction = "Tokyo_Disneyland"

# Initialization of MongoDb server
client = MongoClient("localhost", 27017)
db = client.tripAdvisor
collection = db['comments_at_'+ attraction]

# check the number of documents available in the collection(one document represents one review comment)
print("number of documents inserted :", collection.count())

# convert the bson file into dataframe for analysis
df =  pd.DataFrame(list(collection.find({})))

# Conduct text processing on the reviews for sentiment analysis 
# 1. change to lower case
# 2. remove all the punctuation 
# 3. store the processed string in a new collumn
num = len(df)
df['Processed Comment'] = ""
printable = set(string.printable)

for x in range(num):
    df['Processed Comment'][x] = df['Comment'][x]
    df['Processed Comment'][x] = df['Processed Comment'][x].lower()
    df['Processed Comment'][x] = re.sub(r'[^\w\s]','', df['Processed Comment'][x])
    df['Processed Comment'][x] = ''.join(filter(lambda x: x in printable, df['Processed Comment'][x]))

# import the library for sentiment analysis
from textblob import TextBlob

# For each of the comment, calculate the sentiment polarity and store in a new collumn as sentiment polarity score
df['Sentiment Polarity'] = ""
for x in range(num):
    blob = TextBlob(df['Processed Comment'][x])
    for sentence in blob.sentences:
        df['Sentiment Polarity'][x] = sentence.sentiment.polarity

# Calculate the Pearson correlation between the rating and sentiment polarity score for each comment
df['Rating'] = df['Rating'].astype(int)
df['Sentiment Polarity'] = df['Sentiment Polarity'].astype(float)
rating_sentiment_corr = df['Rating'].corr(df['Sentiment Polarity'])
print("rating & sentiment correlation is: ", rating_sentiment_corr)

# check the minimum, maximum and average sentiment polarity score of the comments
df['Sentiment Polarity'].describe()

# check the median sentiment polarity score of the comments
df['Sentiment Polarity'].median()

# Store and list out all the negative sentiment comments
negative_comment = df[(df['Sentiment Polarity']<0)]
negative_comment['Comment']

# Store and list out all the negative sentiment comments
positive_comment = df[(df['Sentiment Polarity']>0)]
positive_comment['Comment']

# Sort the sentiment polarity score and store as a new column
df_sort = df.sort_values(by=['Sentiment Polarity'], ascending=False)

# check the top 5 positive sentiment comments
df_sort.head(5)

# check the top 5 negative sentiment comments
df_sort.tail(5)

# Understand the text of the interested comment accoding to their sentiment polarity score
df_sort['Comment'][0]

# check the most positive sentiment comments
df[df['Sentiment Polarity'] == df['Sentiment Polarity'].max()]

# check the most negative sentiment comments
df[df['Sentiment Polarity'] == df['Sentiment Polarity'].min()]

# Concatenate all the negative reviews into one huge text file
negative_text_list=""
for x in negative_comment['Comment']:
    negative_text_list += " " + x

# Concatenate all the postive reviews into one huge text file
positive_text_list=""
for x in positive_comment['Comment']:
    positive_text_list += " " + x

### define a function for text preprocessing for wordcloud visualization
def textPreprocess(text_list):
    # Change all the text into lower case for normalization
    text_list = text_list.lower()

    # remove all the not english word or weird word
    printable = set(string.printable)
    text_list = ''.join(filter(lambda x: x in printable, text_list))

    # remove all the punctuation
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text_list)

    # remove all the english stopwords 
    meaningful_words = [word for word in words if word not in stopwords.words('english')]  
    
    return meaningful_words

### define the positive or negative sentiment text list for wordcloud visualization
# postive sentiment = positive_text_list
# negative sentiment = negative_text_list
text_list = positive_text_list

meaningful_words_adjective = []
meaningful_words_noun = []
meaningful_words_verb = []

# tag each of the word in the text list with their grammatically word class
meaningful_words_tag = nltk.pos_tag(textPreprocess(text_list))

# create a new word list from the original word list with only adjective
for word, tag in meaningful_words_tag:
    if tag.startswith('JJ'):
        meaningful_words_adjective.append(word)

# create a new word list from the original word list with only noun
for word, tag in meaningful_words_tag:
    if tag.startswith('NN'):
        meaningful_words_noun.append(word)
        
# create a new word list from the original word list with only verb        
for word, tag in meaningful_words_tag:
    if tag.startswith('VB'):
        meaningful_words_verb.append(word)
        
# join each of the word list into a string       
meaningful_words_string = ' '.join(word for word in textPreprocess(text_list))
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