class Usuario:

    def __init__(self, user, password, email):
        self.user = user
        self.password = password
        self.email = email

    def get_info(self):
        return {
            "user": self.user,
            "password": self.password,
            "email": self.email
        }
