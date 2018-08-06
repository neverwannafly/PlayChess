## Allows you to make your messages more comprehensive

class ComprehensiveMessage:
    
    def __init__(self, message, code, success=False):
        self.message = message
        self.code = code
        self.info = "N/A"

    def message(self):
        return self.message

    def code(self):
        return self.code

    def is_success(self):
        return self.success
