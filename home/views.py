from django.shortcuts import render
from blog.models import Article

def home(request):
    articles = Article.objects.all()
    # recent_articles = Article.objects.all()[:3]

    return render(request, 'home/home.html', {'articles': articles})

