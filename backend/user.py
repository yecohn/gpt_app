from backend.info import info_user

class User:
    def __init__(self, username = 'FirstUser', level = 'beginner') -> None:
        self.username = username
        self.level = level
        self.userInfo = self.retrievePersonalInfo()

    def updatePersonalInfo(self):
        self.userInfo = info_user

    def retrievePersonalInfo(self):
        return info_user

if __name__ == '__main__':
    pass
    user = User('Meir', 'beginner')
    print(user.userInfo['location']['city'])
