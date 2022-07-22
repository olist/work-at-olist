from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from api_books.core.models import Author


PAGE_NUMBER = 1
PAGE_SIZE = 3


def authors(request):

    if request.method == 'GET':

        name = request.GET.get('name')
        if name:
            try:
                author = Author.objects.get(name=name)
                data = author.to_dict()
                return JsonResponse(data)
            except ObjectDoesNotExist:
                return JsonResponse({'error': f'Author with name {name} not found'})

        page_number = int(request.GET.get('page', PAGE_NUMBER))
        page_size = request.GET.get('page_size', PAGE_SIZE)

        queryset = Author.objects.all()

        paginator = Paginator(queryset, page_size)
        page = paginator.page(page_number)

        data = {
            'result': [author.to_dict() for author in page.object_list],
            'count': paginator.count,
            'current_page': page_number
        }

        if page.has_previous():
            n = page.previous_page_number()
            data['previous'] = request.build_absolute_uri(f'/api/authors?page={n}&page_size={page_size}')
        if page.has_next():
            n = page.next_page_number()
            data['next'] = request.build_absolute_uri(f'/api/authors?page={n}&page_size={page_size}')

        return JsonResponse(data)

    return JsonResponse({})
