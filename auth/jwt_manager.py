from jwt import decode, encode


def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="this_key_is_secret", algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    data: dict = decode(token, key="this_key_is_secret", algorithms=["HS256"])
    return data
