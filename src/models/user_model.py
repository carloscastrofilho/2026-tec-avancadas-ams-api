class User:
    
    def __init__(self, id: int = None, namefull: str = "", login: str = "" , password: str = "123", idroller:int = None):
        self.id = id
        self.namefull = namefull
        self.login = login
        self.password = password
        self.idroller = idroller

    def to_dict(self):
        return {
            "id": self.id,
            "namefull": self.namefull,
            "login": self.login,
            "password": self.password,
            "idroller": self.idroller
        }

    @staticmethod
    def from_dict(data: dict):
        return User(
            id=data.get("id"),
            namefull=data.get("namefull"),
            login=data.get("login"),
            password=data.get("password"),
            idroller=data.get("idroller")
            
        )