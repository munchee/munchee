## This is really the Controller part of MVC. Yes this is weird. Very weird.
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .models import *
from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication,
                               PERMISSIONS)
from django.conf import settings

# Create your views here.
def home(request):
    if request.session.get('linkedin_access_token', None):
        return HttpResponseRedirect('/search/')
    else:
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
                                            [PERMISSIONS.BASIC_PROFILE, PERMISSIONS.EMAIL_ADDRESS])
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

            # get profile from LinkedIn
            profile_data = application.get_profile(selectors=['id', 'first-name', 'last-name', 'location', 'industry',
                                                              'email-address', 'summary'])

            # Try to get summary data
            try:
                summary = profile_data['summary']
            except KeyError:
                summary = ''

            # Get existing profile in database
            try:
                profile_db = Profile.objects.get(user_id=profile_data['id'])

                profile_db.user_id=profile_data['id']
                profile_db.first_name=profile_data['firstName']
                profile_db.last_name=profile_data['lastName']
                profile_db.email=profile_data['emailAddress']
                profile_db.summary=summary
                profile_db.industry=profile_data['industry']
                profile_db.location_name=profile_data['location']['name']

            except Profile.DoesNotExist:
                profile_db = Profile(user_id=profile_data['id'], first_name=profile_data['firstName'],
                                 last_name=profile_data['lastName'], email=profile_data['emailAddress'],
                                 summary=summary, industry=profile_data['industry'],
                                 location_name=profile_data['location']['name'])

            # store profile
            profile_db.save()

            # redirect to search page
            return HttpResponseRedirect("/search/")

            #return HttpResponse(str(profile_data))

            # do stuff with application and then return list. Possibly store application in session data
