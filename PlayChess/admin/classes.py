class Admin:

    # A class to create an admin user instant!

    def __init__(self, db):
        self.username = ""
        self.image = ""
        self.password = ""
        self.db = db

    # loads an admin from the databse!
    def loadAdmin(self, username):
        if username is not None:
            admin = self.db.admin.find_one({
                'username': username
            })
            if admin:
                self.username = admin['username']
                self.password = admin['password']
                self.image = admin['image']
            return 0
        return -1
    
    # creates a new admin for the site!
    # This command is only supported through the commandline!
    def createAdmin(self, username, password, image):
        self.db.admin.insert_one({
            'username': username,
            'password': password, 
            'image': image
        })