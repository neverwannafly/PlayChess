# Contains the classes for modeling of various user models.

class User:
    def __init__(self, username, password, email, image, first_name, last_name, rating, db_object):
        self.username = username
        self.password = password
        self.email = email
        self.image = image
        self.first_name = first_name
        self.last_name = last_name
        self.rating = rating
        self.db_object = db_object
    def addUserToDatabase(self):
        dict_object = {
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "username" : self.username,
            "email" : self.email,
            "password" : self.password,
            "image" : self.image,
            "rating" : self.rating
        }
        self.db_object.add_one(dict_object)
        
