# Contains the classes for modeling of various user models.

import random

from ..utils import chessboard

class User:
    # Initialises a user class with a database object!

    """
    NOTE - user id is only used for email verification!
    """

    def __init__(self, _id, first_name, last_name, username, password, email, image, rating, isUserVerified, createdBy, updatedBy, db_object):
        self._id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.image = image
        self.rating = rating
        self.isUserVerified = isUserVerified
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        self.db_object = db_object
        self.in_game = {
            'status': False,
            'url': None,
        }
        self.chessboard = chessboard.Chessboard()

    ## Future update operations would be carried here if required!
    def updateUserRating(self, rating):
        if self.username is not None:
            self.db_object.update_one({
                'username' : self.username,
                },
                {'$set' : {
                    'rating': rating,
                    'updatedBy': "self"}
                },
                upsert=False
            )
            self.rating = rating
            self.updatedBy = "self"
            return 1
        return 0
        
    def updateUserVerificationStatus(self):
        if self.username is not None:
            status = self.db_object.update_one({
                'username': self.username
                },
                {'$set': {
                    'isUserVerified': True,
                    'updatedBy': "self"
                },
                "$currentDate": {"lastModified": True}}
            )
            self.isUserVerified = True
            self.updatedBy = "self"
            return 1
        return 0

def addNewUserToDatabase(username, password, email, image, first_name, last_name, db_object):
    db_object.insert_one({
        "first_name" : first_name,
        "last_name" : last_name,
        "username" : username,
        "email" : email,
        "password" : password,
        "image" : image,
        "rating" : 1200,
        "isUserVerified" : False,
        "createdBy": "self",
        "updatedBy" : "none"
    })

def loadUser(db_object, username):
    user = db_object.find_one({
        'username' : username
    })
    if user is not None:
        _id = str(user['_id'])
        first_name = user['first_name']
        last_name = user['last_name']
        username = user['username']
        password = user['password']
        email = user['email']
        image = user['image']
        rating = user['rating']
        isUserVerified = bool(user['isUserVerified'])
        createdBy = user['createdBy']
        updatedBy = user['updatedBy']
        if isUserVerified==True:
            return (User(_id, first_name, last_name, username, password, email, image, rating, isUserVerified, createdBy, updatedBy, db_object), 1)
        return (User(_id, first_name, last_name, username, password, email, image, rating, isUserVerified, createdBy, updatedBy, db_object), 0)
    return (None, -1)