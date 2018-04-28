# Contains the classes for modeling of various user models.

class User:
    # Initialises a user class with a database object!

    """
    NOTE - Add a initialiser for user id if need arises in future!
    """

    def __init__(self, db_object):
        self.first_name = "N/A"
        self.last_name = "N/A"
        self.username = "N/A"
        self.password = "N/A"
        self.email = "N/A"
        self.image = "N/A"
        self.rating = 1200
        self.isUserVerified = False
        self.db_object = db_object

    def addNewUserToDatabase(self, username, password, email, image, first_name, last_name):
        self.db_object.insert_one({
            "first_name" : first_name,
            "last_name" : last_name,
            "username" : username,
            "email" : email,
            "password" : password,
            "image" : image,
            "rating" : 1200,
            "isUserVerified" : False
        })
    
    def loadUser(self, username):
        user = self.db_object.find_one({
            'username' : username
        })
        if user is not None:
            if user['isUserVerified']==True:
                self.first_name = user['first_name']
                self.last_name = user['last_name']
                self.username = user['username']
                self.password = user['password']
                self.email = user['email']
                self.image = user['image']
                self.rating = user['rating']
                self.isUserVerified = user['isUserVerified']
                return 1
            return 0
        return -1

    def deleteUser(self):
        if self.username is not None:
            self.db_object.delete_one({
                'username' : self.username
            })
            return 1
        return 0

    ## Future update operations would be carried here if required!
    def updateUserRating(self, rating):
        if self.username is not None:
            self.db_object.update_one({
                'username' : self.username,
                '$set' : {'rating': rating},
                '$currentDate': {'lastModified': True}
            })
            return 1
        return 0
