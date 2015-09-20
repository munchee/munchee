## This is really the Controller part of MVC. Yes this is weird. Very weird.
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .models import *
from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication,
                               PERMISSIONS)
from django.conf import settings
from .scrapers import *
from .text_mine import get_most_occured, get_match_percentage, stemmed_top_user_words
import wikipedia

# Create your views here.
def home(request):
    if request.session.get('linkedin_access_token', None):
        return HttpResponseRedirect('/search/')
    else:
        return render(request, 'munchee/home.html', {})

def logout(request):
    if request.session.get('linkedin_access_token'):
        del request.session['linkedin_access_token']
    if request.session.get('linkedin_userid'):
        del request.session['linkedin_userid']
    return HttpResponseRedirect("/")

def search(request):
    debug = ""
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company_dbs = []
            company_ratings = {}
            #return HttpResponse("Is valid \n" + str(form.cleaned_data.keys()))
            companies = [x.strip() for x in form.cleaned_data['companies'].split(',')]
            keywords = [x.strip() for x in form.cleaned_data['keywords'].split(',')]

            user_db = Profile.objects.get(user_id=request.session['linkedin_userid'])
            user_text = ' '.join([user_db.summary, user_db.industry, user_db.location_name])
            user_text = ' '.join(keywords) + ' ' + user_text
            user_words = stemmed_top_user_words(user_text,10)

            for company in companies:
                do_not_modify = False
                ## start hitting multiple sites
                # LinkedIn
                data = scrape_linkedin_company(request.session['linkedin_access_token'], company)
                debug += str(data)
                try:
                    if data['companies']['_count'] == 0:
                        continue
                except KeyError:
                    continue
                # gonna take the first one lol
                the_company = data['companies']['values'][0]
                company_id = the_company['id']


                # get the company entry in database, if any
                try:
                    company_db = Company.objects.get(id=company_id)
                    if company_db.last_updated - timezone.now() < timezone.timedelta(days=1):
                        do_not_modify = True
                except Company.DoesNotExist:
                    company_db = Company()

                name = the_company['name']
                website = the_company['websiteUrl']
                raw_locations = the_company['locations']
                if raw_locations['_total'] == 0:
                    locations = []
                else:
                    locations = [x['address']['city'] for x in raw_locations['values']]
                ticker = the_company.get('ticker', "")
                description = the_company['description']
                logo_url = the_company['logoUrl']

                # Google
                news = '' # temporary empty

                if not do_not_modify:
                    company_db.id = company_id
                    company_db.name = name
                    company_db.website = website
                    company_db.locations = ','.join(locations)
                    company_db.ticker = ticker
                    company_db.description = description
                    company_db.logo_url = logo_url
                    company_db.news = news

                    company_db.save()

                company_dbs.append(company_db)

                # text mining/analysis
                company_text = ' '.join([company_db.locations,description,news,\
                               wikipedia.page(company_db.name+', company').summary])
                company_ratings[company_id] = get_match_percentage(company_text,user_words)
                company_db.score = company_ratings[company_id]
            debug = "" # clear debug because too lazy to remove
            return render(request, "munchee/results.html", {"companies": company_dbs, "ratings": company_ratings, "debug": debug})
            #return HttpResponse(debug + "<br><br><br>")

    elif request.session.get('linkedin_access_token', None):
        form = CompanyForm()
    else:
        return HttpResponseRedirect("/")

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
                                            [PERMISSIONS.BASIC_PROFILE, PERMISSIONS.EMAIL_ADDRESS])
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

            request.session['linkedin_userid'] = profile_data['id']

            # redirect to search page
            return HttpResponseRedirect("/search/")

            #return HttpResponse(str(profile_data))

            # do stuff with application and then return list. Possibly store application in session data
