import re
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

def validate_email(email) -> bool:
    return bool(
        bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))
        and not CustomUser.objects.filter(email=email).exists()
    )



def password_validation(password: str):
    if len(password) < 6:
        return "Password must be at least 6 characters long"
    elif not re.search("[a-z]", password):
        return "Password must have at least one lowercase letter"
    elif not re.search("[0-9]", password):
        return "Password must have at least one digit"
    elif not re.search(r"[\W_]", password):
        return "Password must have at least one special character"
    else:
        return True
    


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

