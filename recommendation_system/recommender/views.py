from django.contrib import messages
from django.shortcuts import render
from .utils.luscher import Luscher
from .utils.movie_recommendation import MovieRecommendation
from .utils.music_recommendation import MusicRecommendation


def index(request):
    context = {
        'page_title': 'Welcome!'
    }
    return render(request, 'recommender/index.html', context)


def result(request):
    context = {
        'page_title': 'Result',
    }

    if request.method == 'POST':
        sequence = request.POST.get('sequence')
        sequence = [int(x) for x in sequence.split(',')]
        luscher = Luscher(sequence)
        recommender = MusicRecommendation()
        mood = luscher.get_interpretation()
        recommendation = recommender.get_songs_for_mood(mood)
        artists = recommendation['artist.name'].tolist()
        titles = recommendation['title'].tolist()
        context['music_recommendation'] = dict(zip(artists, titles))
        messages.success(request, f"Looks like you feel {mood}. Here's some music for you!")


    return render(request, 'recommender/result.html', context)