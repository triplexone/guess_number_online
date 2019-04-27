from smartninja_nosql.odm import Model

class User(Model):
    def __init__(self, name, email, secret, **kwargs):
        self.name = name
        self.email = email
        self.secret = secret

        super().__init__(**kwargs)