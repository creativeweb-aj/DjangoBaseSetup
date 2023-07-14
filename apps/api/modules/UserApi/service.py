from apps.users.models import User


class UserQueryService:
    def __init__(self):
        pass

    @staticmethod
    def createUser(data):
        user = User()
        user.user_role_id = 2  # This is normal UserApi role id is 2
        user.first_name = data.get('first_name', None)
        user.last_name = data.get('last_name', None)
        user.username = data.get('username', None)
        user.email = data.get('email', None)
        user.password = data.get('password', None)
        user.confirm_password = data.get('confirm_password', None)
        user.save()

    @staticmethod
    def updateUser(id, data):
        user = User.objects.filter(id=id).first()
        user.user_role_id = 2  # This is normal UserApi role id is 2
        user.first_name = data.get('first_name', None)
        user.last_name = data.get('last_name', None)
        user.username = data.get('username', None)
        user.email = data.get('email', None)
        user.password = data.get('password', None)
        user.confirm_password = data.get('confirm_password', None)
        user.save()

    @staticmethod
    def getUserById(value):
        result = User.objects.filter(id=value).first()
        return result

    @staticmethod
    def getUserByUsername(value):
        result = User.objects.filter(username=value).first()
        return result

    @staticmethod
    def getUserByEmail(value):
        result = User.objects.filter(email=value).first()
        return result

    @staticmethod
    def getUserByMobile(value):
        result = User.objects.filter(mobile=value).first()
        return result
