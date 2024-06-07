from itsdangerous import URLSafeTimedSerializer
from app.config import Config

def encode_id(id):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(id)

def decode_id(token):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        book_id = serializer.loads(token, max_age=3600)  # max_age para expiração do token
        return book_id
    except Exception as e:
        print(f"Erro ao decodificar book_id: {e}")
        return None
