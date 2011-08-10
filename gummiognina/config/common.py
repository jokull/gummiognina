import os

DEFAULT_MAIL_SENDER = 'noreply@gummiognina.com'

ADMINS = MANAGERS = ['jokull@solberg.is']

UPLOADS_DEFAULT_DEST = os.environ.get('UPLOADS_PATH', '/tmp/uploads')

SECRET_KEY = 'developer-key'

UPLOADS_DEFAULT_URL = '/uploads/'