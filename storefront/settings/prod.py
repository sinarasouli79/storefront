# noinspection PyUnresolvedReferences
import os

from .common import *

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = []
