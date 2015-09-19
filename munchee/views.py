from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import *

# Create your views here.
def home(request):
    return render(request, 'munchee/home.html', {})

def search(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            return HttpResponse("Is valid" + form.cleaned_data)
    else:
        form = CompanyForm()
        
    return render(request, 'munchee/search.html', {})
