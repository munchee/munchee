import wikipedia
from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication,
                               PERMISSIONS)

def wikipedia_summary(company):
    return wikipedia.summary(company + " company")

def scrape_linkedin_company(token, company):
    application = LinkedInApplication(token=token)
    company_data = application.search_company(selectors=[{'companies': ['name', 'id',
                                                         'website-url', 'industries', 'locations', 'logo-url',
                                                         'specialties', 'description', 'ticker']}],
                                              params={'keywords': company})
    return company_data


###DO NOT USE BELOW
def scrape_linkedin_company_search(token, keywords):
    application = LinkedInApplication(token)
    company_data = application.search_company(selectors=[{'companies': ['name', 'universal-name',
                                                         'website-url', 'industry', 'location', 'summary']}],
                               params={'keywords', keywords})

    return company_data
