from django.urls import path
from . import views
from .views import ajouter_commentaire

urlpatterns = [
    # Autres URLs de l'application
    path('recette/<int:pk>/', views.detail_recette, name='detail_recette'),
    path('<int:pk>/ajouter_commentaire/', ajouter_commentaire, name='ajouter_commentaire'),
    path('commentaire/<int:pk>/dislike', views.ajouter_dislike, name='ajouter_dislike'),
    path('commentaire/<int:pk>/like', views.ajouter_like, name='ajouter_like'),
    path('', views.recette_list, name='liste_recettes'),
    path('<int:pk>/supprimer/', views.supprimer_recette, name='suppression_recette'),
    path('creer', views.creer_recette, name='creer_recette'),


]