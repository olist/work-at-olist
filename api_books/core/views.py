from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from api_books.core.models import Author


def authors(resquest):

    if resquest.method == 'GET':

        name = resquest.GET.get('name')
        if name:
            try:
                author = Author.objects.get(name=name)
                data = author.to_dict()
                return JsonResponse(data)
            except ObjectDoesNotExist:
                return JsonResponse({'error': f'Author with name {name} not found'})

        data = {
            'list': [author.to_dict() for author in Author.objects.all()]
        }

        return JsonResponse(data)

    return JsonResponse({})
