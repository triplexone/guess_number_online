from smartninja_nosql.odm import Model

class User(Model):
    def __init__(self, name, secret, **kwargs):
        self.name = name
        self.secret = secret

        super().__init__(**kwargs)