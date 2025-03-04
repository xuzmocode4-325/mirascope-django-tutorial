from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path('', views.IndexView.as_view(), name='joke_explainer_index'),
]