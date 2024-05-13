from datetime import datetime, timedelta, timezone
from .models import Token as TokenModel
from random import choice
from string import hexdigits

class Token:
    def __init__(self, token: str) -> None:
        self.token = token

    def check(self) -> bool:
        try:
            token = TokenModel.objects.get(token=self.token)
            return datetime.now(timezone.utc) < token.exp_in

        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def new_token():
        token = ''.join([choice(hexdigits) for _ in range(200)])
        exp_in = datetime.now() + timedelta(days=7)
        token_model_instanse = TokenModel(token=token, exp_in=exp_in)
        
        return token_model_instanse
