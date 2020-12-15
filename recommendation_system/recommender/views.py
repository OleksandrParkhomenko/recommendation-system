from django.shortcuts import render


def index(request):
    context = {
        'page_title': 'Welcome!'
    }
    return render(request, 'recommender/index.html', context)
