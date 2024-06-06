from itsdangerous import URLSafeTimedSerializer
from app.config import Config
def enconde_book_id(book_id):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(book_id)

def decode_book_id(token):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        book_id = serializer.loads(token)
        return book_id
    except:
        return None