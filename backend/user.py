from backend.info import dict

class User:
    def __init__(self, username = 'FirstUser', level = 'beginner') -> None:
        self.username = username
        self.level = level
        self.userInfo = self.retrievePersonalInfo()

    def updatePersonalInfo(self):
        self.userInfo = dict

    def retrievePersonalInfo(self):
        return dict

if __name__ == '__main__':
    pass
    user = User('Meir', 'beginner')
    print(user.userInfo['location']['city'])
