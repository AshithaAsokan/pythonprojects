from django.shortcuts import render
from django.views.decorators.cache import cache_page

@cache_page(60*1)  #60 second
def home(request):
    return render(request,'index.html')
