from django.http import JsonResponse

from api_books.core.models import Author


def authors(resquest):

    data = {
        'list': [author.to_dict() for author in Author.objects.all()]
    }

    return JsonResponse(data)
