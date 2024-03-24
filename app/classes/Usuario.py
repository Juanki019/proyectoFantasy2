class Usuario:

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def get_info(self):
        return {
            "user": self.username,
            "password": self.password,
            "email": self.email
        }
