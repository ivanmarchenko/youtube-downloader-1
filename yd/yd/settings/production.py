from yd.settings.common import *

# production

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['ytd.pythonanywhere.com']