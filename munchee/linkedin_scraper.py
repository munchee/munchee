from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication,
                               PERMISSIONS)

API_KEY = '77xaacj4a17451'
API_SECRET = 'rPjQxiuofXfbro6C'
RETURN_URL = 'http://localhost:8000/complete/linkedin-oauth2/'
authentication = LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL,
                                        PERMISSIONS.enums.values())

print(authentication.authorization_url)
application = LinkedInApplication(authentication)