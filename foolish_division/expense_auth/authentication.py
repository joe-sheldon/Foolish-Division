from rest_framework.authentication import TokenAuthentication


class FoolishTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'  # Change the prefix to 'Bearer'