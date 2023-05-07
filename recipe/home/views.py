from django.shortcuts import render
from recette.models import Recette
from notes.models import Note
from django.db.models import Avg


def home(request):
    recettes = Recette.objects.all()
    for recette in recettes:
        note_moyenne = Note.objects.filter(recette=recette).aggregate(Avg('valeur'))['valeur__avg']
        recette.note_moyenne = note_moyenne
    context = {
        'recettes': recettes
    }
    return render(request, 'home_page.html', context)
