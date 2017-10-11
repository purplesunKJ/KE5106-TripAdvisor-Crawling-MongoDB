
from pymongo import MongoClient
from bson import ObjectId

class REVIEW:
    def __init__(self, attraction):
        self.username = ''
        self.location = ''
        self.title = ''
        self.comment = ''
        self.visitedDate = ''
        self.postedDate = ''
        self.rate = ''
        self.tripAtWhere = 'comments_at_'+ attraction

    def setUsername(self, name):
        self.username = name

    def getUsername(self):
        return self.username

    def setLocation(self, loc):
        self.location = loc

    def setTitle(self, title):
        self.title = title

    def setComment(self, comment):
        self.comment = comment

    def setVisitedDate(self, date):
        self.visitedDate = date

    def setPostedDate(self, date):
        self.postedDate = date

    def setRate(self, rate):
        self.rate = rate

    def setAttractionAtWhere(self, attraction):
        self.tripAtWhere = self.tripAtWhere+attraction

    def getAttractionAtWhere(self):
        return self.tripAtWhere

    def getReviewer(self, reviewerId, commentId):
        data ={}
        data['_id'] = reviewerId
        data['User name'] = self.username
        data['Location'] = self.location
        if(type(commentId) is list):
            data['Comments_Id'] = commentId
        else:
           data['Comments_Id'] = [commentId]
        return data

    def getComment(self, reviewerId, commentId):
        data = {}
        data['_id'] = commentId
        data['User Id'] = reviewerId        
        data['Title'] = self.title
        data['Month of Visit'] = self.visitedDate
        data['Date Posted'] = self.postedDate
        data['Rating'] = self.rate
        data['Comment'] = self.comment
        return data

class tripAdvisorDB:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.tripAdvisor

    #post a review object into mongodb
    def post(self, REVIEW):
        #find whether the reviewer is existed or not 
        reviewer = self.db['reviewers'].find({"User name":REVIEW.getUsername()});
        if(reviewer.count()>0):
            #update existed reviewer and insert a new comment
            new_comment_id = ObjectId()
            cur_reviewer_id = reviewer[0]['_id']
            comments_id = reviewer[0]['Comments_Id']
            comments_id.append(new_comment_id)
            self.db['reviewers'].update({'_id':cur_reviewer_id},REVIEW.getReviewer(cur_reviewer_id,comments_id))
            new_comment_id = self.db[REVIEW.getAttractionAtWhere()].insert(REVIEW.getComment(cur_reviewer_id,new_comment_id))
            #print("insert a new comment : " , new_comment_id)
            #print("update a new reviewer : " , cur_reviewer_id)
        else :
            #insert a new reviewer and a new comment
            new_comment_id = ObjectId()
            new_reviewer_id = ObjectId()
            new_comment_id = self.db[REVIEW.getAttractionAtWhere()].insert(REVIEW.getComment(new_reviewer_id,new_comment_id))
            new_reviewer_id = self.db['reviewers'].insert(REVIEW.getReviewer(new_reviewer_id,new_comment_id))
            #print("insert a new comment : " , new_comment_id)
            #print("insert a new reviewer : " , new_reviewer_id)

    #recusively go throught enitre database
    def recusive(self, limit):
        print("")
        for c in self.db.collection_names(include_system_collections=False):            
            print(c," has ", self.db[c].find().count(), " documents")
            print("sample records in ", c, ", limited number at ", limit)
            if(limit<0):
                for record in self.db[c].find():
                    print(record)
                print("")
            else:
                for record in self.db[c].find().limit(limit):
                    print(record)
                print("")           

    #clean all the data in database
    def clean(self):
        for c in self.db.collection_names(include_system_collections=False):
            self.db[c].delete_many({})
            self.db[c].drop()