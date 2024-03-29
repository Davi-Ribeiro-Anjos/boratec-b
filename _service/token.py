import jwt
import random
import string
import bcrypt

from _app.settings import SECRET_KEY
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from employees.models import Employees
from employees.serializers import EmployeesLoginSerializer


# TOKEN - LOGIN
def create_token_login(token):
    try:
        user_id = token.get("user_id")

        employee = get_object_or_404(Employees, user_id=user_id)

        token["employee"] = dict(EmployeesLoginSerializer(employee).data)

        return jwt.encode(token, SECRET_KEY, algorithm="HS256")
    except Exception:
        return jwt.encode(token, SECRET_KEY, algorithm="HS256")


# TOKEN - EMAIL


def random_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_token_email(dict_token):
    return jwt.encode(dict_token, SECRET_KEY, algorithm="HS256")


def decode_token_email(token):
    return jwt.decode(token, SECRET_KEY, algorithms="HS256")
