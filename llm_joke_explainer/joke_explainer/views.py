from django.views.generic import TemplateView
from mirascope import llm
from django.http import JsonResponse

# Create your views here.
class IndexView(TemplateView):
    template_name = 'joke_explainer/index.html'



