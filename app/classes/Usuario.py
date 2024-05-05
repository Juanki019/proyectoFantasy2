class Usuario:

    def __init__(self, username, password, email, profile):
        self.username = username
        self.password = password
        self.email = email
        self.profile = profile

    def get_info(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "profile": self.profile
        }
