# Azure prod-specific variables config
DEBUG = False
ALLOWED_HOSTS = ["munchee.azurewebsites.net", "mchee.co"]
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = os.environ["LINKEDIN_KEY"]
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = os.environ["LINKEDIN_SECRET"]
SECRET_KEY = os.environ["DJANGO_KEY"]