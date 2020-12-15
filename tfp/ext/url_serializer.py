from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer

url_serializer = None
url_timed_serializer = None


def init_app(app):
    global url_serializer, url_timed_serializer
    url_serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    url_timed_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
