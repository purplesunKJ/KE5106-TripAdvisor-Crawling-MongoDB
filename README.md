# KE5106-TripAdvisor-Crawling-MongoDB
CA for KE5106 Data Warehousing for Business Analytics

Current Challenges 

Every backpacker must have heard about TripAdvisor. Almost every backpacker will use the platform to conduct travel research to decide which attraction to go. Many of the well-known attractions at Japan have been reviewed and rated by thousands of past travelers and it will be useful for prospective traveler who plan to visit Japan to be able to get some insights from the thousands rating and reviews submitted efficiently.

However, although the platform is resourceful, most users have difficulties to have an overview on the review comment or extract the negative comments from thousands of reviews submitted as there are far more positive comment as compared to negative comment. 

In fact, many users agree that there are more preparation and consideration can be done from reading the negative sentiment reviews. As for the attraction management committee, negative sentiment reviews are valuable for them as it can provide a useful insight to assist in the decision-making process to improve the services and facilities of attractions. Given that there are thousands of reviews available and usually only a small amount of the reviews carried a negative sentiment polarity, it is always a challenge for both prospective travelers and attraction management committee to make use of the reviews for their interest.

Hence, the business objective of this project is to figure out the key phrases and understand the sentiment associated with traveler’s satisfactions of the services provided by various attractions in Japan from their submitted reviews. 
 
Proposed Solution

This project aim to scrape travelers’ reviews from the TripAdvisor website and stored them as desired schema in MongoDB before proceed for further analysis. The reviews for five famous attractions in Japan for a period of a year has been scrapped. The five attractions are:

1.	Fushimi Inari Shrine
2.	Hiroshima Peace Memorial Park
3.	Jigokudani Snow Monkey Park
4.	Kiyomizu Dera
5.	Tokyo Disneyland

Two parts of analysis have been conducted on the stored reviews for each attraction. The first part involves text mining on the reviews and extract the key phrases to construct a word cloud for each attraction. This allow prospective traveler to have a glimpse on the reviews on an attraction in Japan. Second part of the analysis involve the sentiment analysis in which a sentiment polarity score for each of the reviews has been calculated. This allow the prospective traveler to extract the negative sentiment reviews easily from thousands of reviews.
