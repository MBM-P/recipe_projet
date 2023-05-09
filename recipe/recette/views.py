from django.shortcuts import render, get_object_or_404,redirect
from recette.models import Recette
from etapes.models import Etape
from notes.models import Note
from commentaires.models import Commentaire
from django.db import models
from notes.forms import NoteForm
from django.contrib.auth.decorators import login_required
from commentaires.forms import CommentaireForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import RecetteForm
from django.core.paginator import Paginator

@login_required
def ajouter_commentaire(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.user = request.user
            commentaire.recette = recette
            commentaire.save()
            messages.success(request, 'Commentaire ajouté avec succès')
            return redirect('detail_recette', pk=pk)
    else:
        form = CommentaireForm()
    return render(request, 'ajouter_commentaire.html', {'form': form})

@login_required
def ajouter_note(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.recette = recette
            note.user = request.user
            note.save()
            return redirect('detail_recette', pk=pk)
    else:
        form = NoteForm()
    context = {'form': form}
    return render(request, 'ajouter_note.html', context)

def detail_recette(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    etapes = Etape.objects.filter(recette=recette).order_by('ordre')
    note_moyenne = Note.objects.filter(recette=recette).aggregate(models.Avg('valeur'))['valeur__avg']
    commentaires = Commentaire.objects.filter(recette=recette).order_by('-date')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.recette = recette
            note.user = request.user
            note.save()
            return redirect('detail_recette', pk=pk)
    else:
        form = NoteForm()

    commentaire_form = CommentaireForm()

    context = {
        'recette': recette,
        'etapes': etapes,
        'note_moyenne': note_moyenne,
        'commentaires': commentaires,
        'form': form,
        'commentaire_form': commentaire_form,
    }

    return render(request, 'detail_recette.html', context)
@login_required
def ajouter_like(request, pk):
    commentaire = get_object_or_404(Commentaire, pk=pk)
    commentaire.likes += 1
    commentaire.save()
    messages.success(request, "Le commentaire a été liké avec succès.")
    return redirect('detail_recette', pk=commentaire.recette.pk)
@login_required
def ajouter_dislike(request, pk):
    commentaire = get_object_or_404(Commentaire, pk=pk)
    commentaire.dislikes += 1
    commentaire.save()
    messages.success(request, "Le commentaire a été disliké avec succès.")
   
    return redirect('detail_recette', pk=commentaire.recette.pk)

def recette_list(request):
    recettes = Recette.objects.all()
    p= Paginator(Recette.objects.all(),6)
    page = request.GET.get('page')
    recipe = p.get_page(page)
    return render(request, 'recette_list.html', {'recettes': recettes,'recipe':recipe})



def creer_recette(request):
    if request.method == 'POST':
        form = RecetteForm(request.POST, request.FILES)
        if form.is_valid():
            recette = form.save(commit=False)
            recette.auteur = request.user
            recette.save()
            return redirect('detail_recette', pk=recette.pk)
    else:
        form = RecetteForm()
    return render(request, 'creer_recette.html', {'form': form})



def supprimer_recette(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    if request.user == recette.auteur:
        recette.delete()
        return redirect('liste_recettes')
    else:
        return redirect('detail_recette', pk=pk)    