from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .models import *
from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication,
                               PERMISSIONS)
from django.conf import settings
import json

# Create your views here.
def home(request):
    return render(request, 'munchee/home.html', {})

def search(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            #return HttpResponse("Is valid \n" + str(form.cleaned_data.keys()))
            cleaned_info = form.cleaned_data
            print(cleaned_info)
    else:
        form = CompanyForm() 

    return render(request, 'munchee/search.html', {})

def oauth_login_start(request):
    authentication = LinkedInAuthentication(settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
                                            settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET,
                                            settings.RETURN_URL,
                                            PERMISSIONS.enums)
    return HttpResponseRedirect(authentication.authorization_url)

def oauth_callback(request):
    authentication = LinkedInAuthentication(settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
                                            settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET,
                                            settings.RETURN_URL,
                                            PERMISSIONS.enums.values())
    if request.method == 'GET':
        form = OAuthCallbackForm(request.GET)
        if form.is_valid():
            """cleaned_code = form.cleaned_data['code']
            cleaned_state = form.cleaned_data['state']
            return HttpResponse("Code: " + cleaned_code + "\nState: " + cleaned_state)"""
            authentication.authorization_code = form.cleaned_data['code']
            token = authentication.get_access_token()

            # store access token in session
            request.session['linkedin_access_token'] = token

            application = LinkedInApplication(token=token)

            # get profile
            profile_raw = application.get_profile()

            profileinfo = json.loads(profile_raw)

            return HttpResponse(profile_raw)

            # do stuff with application and then return list. Possibly store application in session data
