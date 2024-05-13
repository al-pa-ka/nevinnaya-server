from enum import Enum, auto
from .models import Admin as AdminModel, Token as TokenModel
from abc import ABC
from .token import Token
from rest_framework.response import Response

class Permissions(Enum):
    CAN_CREATE_GOODS = auto()


class User(ABC):
    def get_permissions(self) -> list[str]:...

    def authentificate(self, login: str, password: str) -> bool:...

class Admin(User):

    def get_permissions(self) -> list[str]:
        [permission.name for permission in Permissions]

    @staticmethod
    def is_aunteficated(function: callable):
        def wrapper(self, request, *args, **kwargs):
            try:
                token = TokenModel.objects.get(token=request.data['token'])
                admin_user = token.user
                if (admin_user and Token(token.token).check()):
                    return function(self, request, *args, **kwargs)
            except Exception as e:
                print(e)
                return Response(data='no permissions', status=403)
        return wrapper

    def authentificate(self, login: str, password: str) -> str | None:
        try:
            admin = AdminModel.objects.get(login=login, password=password)
            token = Token.new_token()
            if admin.token:
                return admin.token.token
            admin.token = token
            token.save()
            admin.save()
            return admin.token.token
        except Exception as e:
            print(e)
            return None

