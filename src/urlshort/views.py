from django.shortcuts import render, redirect as django_redirect
from .models import ShortURL
from .forms import CreateNewShortURL
from datetime import datetime
import random, string

def home(request):
    return render(request, 'home.html')

def redirect(request, url):
    current_obj = ShortURL.objects.filter(short_url=url)
    if len(current_obj) == 0:
        return render(request, 'pagenotfound.html')
    context = {'obj': current_obj[0]}
    return render(request, 'redirect.html', context)

def createShortURL(request):
    if request.method == 'POST':
        form = CreateNewShortURL(request.POST)
        if form.is_valid():
            original_website = form.cleaned_data['original_url']
            random_chars = ''.join(random.choices(string.ascii_letters, k=6))
            while ShortURL.objects.filter(short_url=random_chars).exists():
                random_chars = ''.join(random.choices(string.ascii_letters, k=6))
            s = ShortURL(original_url=original_website, short_url=random_chars, time_date_created=datetime.now())
            s.save()
            return render(request, 'urlcreated.html', {'chars': random_chars})
    else:
        form = CreateNewShortURL()
    return render(request, 'create.html', {'form': form})
