class Admin:

    # A class to create an admin user instant!

    def __init__(self, db):
        self.admin_username = ""
        self.admin_password = ""
        self.db = db

    # loads an admin from the databse!
    def loadAdmin(self, admin_username):
        if admin_username is not None:
            admin = self.db.admin.find_one({
                'admin_username': username
            })
            if admin:
                self.admin_username = admin['username']
                self.admin_password = admin['password']
            return 0
        return -1
    
    # creates a new admin for the site!
    # This command is only supported through the commandline!
    def createAdmin(self, admin_username, admin_password):
        self.db.admin.insert_one({
            'admin_username': admin_username,
            'admin_password': admin_password
        })

    def createUser()