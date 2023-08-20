import jwt

from _app.settings import SECRET_KEY
from django.contrib.auth.models import User

from users.serializers import UserLoginSerializer


def custom_payload_handler(token):
    user_id = token.get("user_id")
    user = User.objects.get(id=user_id)

    token["employee"] = dict(UserLoginSerializer(user).data)

    return jwt.encode(token, SECRET_KEY, algorithm="HS256")
    # print(token)
    # print(jwt.encode(token, SECRET_KEY, algorithm="HS256"))
