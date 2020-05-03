from django.http import HttpResponse

# Create your views here.
from olist.library.models import Author


def home(request):
    return HttpResponse('<html><body>Ola django</body></html>', content_type='text/html')


def author(request, name):
    return Author.objects.get(name=name)
