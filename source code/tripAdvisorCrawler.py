# import libraries 
import requests
import datetime
from bs4 import BeautifulSoup

# import self define libraries 
from tripAdvisorDB import REVIEW
from tripAdvisorDB import tripAdvisorDB

# initialize mongodb operations
tripdb = tripAdvisorDB()

### Only run if wan to clean the database and reextract the data
tripdb.clean()

# define the range in days the review comments to be extracted
RangeOfDay = 365

# define the attraction to be extracted and their seed url
JapanAttractionListAndSeedURL = [
    ["Fushimi_Inari_Shrine",
     "https://www.tripadvisor.com.sg/ShowUserReviews-g298564-d321456-r515364769-Fushimi_Inari_taisha_Shrine-Kyoto_Kyoto_Prefecture_Kinki.html#REVIEWS"],
    ["Hiroshima_Peace_Memorial_Park",
     "https://www.tripadvisor.com.sg/ShowUserReviews-g298561-d1165220-r513425593-Hiroshima_Peace_Memorial_Park-Hiroshima_Hiroshima_Prefecture_Chugoku.html#REVIEWS"],
    ["Jigokudani_Snow_Monkey_Park", 
     "https://www.tripadvisor.com.sg/ShowUserReviews-g1117904-d324924-r513787085-Jigokudani_Snow_Monkey_Park-Yamanouchi_machi_Shimotakai_gun_Nagano_Prefecture_Ch.html#REVIEWS"],
    ["Kiyomizu_Dera", 
     "https://www.tripadvisor.com.sg/ShowUserReviews-g298564-d321401-r514547649-Kiyomizu_dera_Temple-Kyoto_Kyoto_Prefecture_Kinki.html#REVIEWS"],
    ["Tokyo_Disneyland",
     "https://www.tripadvisor.com.sg/ShowUserReviews-g298162-d320634-r515028373-Tokyo_Disneyland-Urayasu_Chiba_Prefecture_Kanto.html#REVIEWS"]
]

# while loop to scrape data according to the range defined

for attraction in JapanAttractionListAndSeedURL[:]:
    date_posted = datetime.datetime.strftime(datetime.datetime.now(), '%d %B %Y')
    url = attraction[1]
    
    # indicate the start of date scraping for each location
    print("Scraping " + attraction[0] + ".....")
    
    while (datetime.datetime.now() - datetime.datetime.strptime(date_posted, '%d %B %Y') <= datetime.timedelta(RangeOfDay)):

        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        container_review = soup.find('div',id='REVIEWS')

        # extract username & user location
        names = container_review.findAll('div', class_='member_info') 

        # extract review titles
        titles = container_review.findAll('div',class_='quote')

        # extract ratings and date posted
        ratings = container_review.findAll('div', class_='rating reviewItemInline')

        # extract reviews
        reviews = container_review.findAll('p')

        # extract visit month
        month_visit = container_review.findAll('span', class_='recommend-titleInline noRatings')

        oneReview = REVIEW(attraction[0])
        num=len(reviews)
        for j in range(num):

            # print username
            if len(names[j].findAll('div',class_="username mo"))!=0:
                username = names[j].find('div', class_="username mo").text.strip()
            else:
                username = 'Anonymous member'
            #print ('Username: ',username)
            oneReview.setUsername(username)

            # print user location
            if len(names[j].findAll('div',class_="location"))!=0:
                location = names[j].find('div', class_="location").text.strip()
            else:
                location = 'Unavailable'
            #print ('Location: ',location)
            oneReview.setLocation(location)

            #print review titles
            #print('Title: ',titles[j].text.strip())
            oneReview.setTitle(titles[j].text.strip())

            #print ratings
            #print('Ratings: ',ratings[j].find('span').get('class')[1][7])
            oneReview.setRate(ratings[j].find('span').get('class')[1][7])

            #print date posted
            #the class attributes from page 9 onward is different hence need condition check
            if(ratings[j].find('span', class_="ratingDate").get("title")):
                date_posted = ratings[j].find('span', class_="ratingDate relativeDate").get("title")
            elif(ratings[j].find('span', class_="ratingDate")):
                date_posted = ratings[j].find('span', class_="ratingDate").text.strip()[9:]
            #print('Date Posted: ',date_posted)
            oneReview.setPostedDate(date_posted)

            #print review
            #print('Review: ',reviews[j].text.strip())
            oneReview.setComment(reviews[j].text.strip())

            #print month visited
            #print('Month of Visit: ',month_visit[j].text.strip()[8:])
            oneReview.setVisitedDate(month_visit[j].text.strip()[8:])        

            tripdb.post(oneReview)        

        # grab the next url
        container_next_page=soup.find('div',class_='unified pagination ')
        nexturl=container_next_page.findAll('a')[1].get('href')
        url='https://www.tripadvisor.com.sg/'+ nexturl
        
    # indicate the end of data scraping for each location
    print("Finished Scraped " + attraction[0] + "!!!")

# Check and verify the first 10 documents for reviewers and attractions collections in mongoDb
if __name__ == '__main__':
    tripdb.recusive(10)
