from munchee.settings import *
# Azure prod-specific variables config
DEBUG = False
ALLOWED_HOSTS = ["munchee.azurewebsites.net", "mchee.co"]
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = os.environ["LINKEDIN_KEY"]
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = os.environ["LINKEDIN_SECRET"]
SECRET_KEY = os.environ["DJANGO_KEY"]

### log Django errors to the root of your Azure Website
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.RequireDebugFalse'
    }
  },
  'handlers': {
    'logfile': {
      'class': 'logging.handlers.WatchedFileHandler',
      'filename': 'D:/home/site/wwwroot/error.log'
    },
  },
  'loggers': {
    'django': {
      'handlers': ['logfile'],
      'level': 'ERROR',
      'propagate': False,
    },
  }
}
