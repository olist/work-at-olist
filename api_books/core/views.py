from django.http import JsonResponse
from django.core.paginator import Paginator
from api_books.core.links import LinkPaginator

from api_books.core.models import Author, Book


PAGE_NUMBER = 1
PAGE_SIZE = 3


def authors(request):

    if request.method == 'GET':

        page_number = int(request.GET.get('page', PAGE_NUMBER))
        page_size = request.GET.get('page_size', PAGE_SIZE)

        queryset = Author.objects.all()

        name = request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        paginator = Paginator(queryset, page_size)
        page = paginator.page(page_number)

        result = [author.to_dict() for author in page.object_list]
        if not result:
            return JsonResponse({'error': f'Author with name {name} not found'})

        data = {
            'result': result,
            'count': paginator.count,
            'current_page': page_number
        }

        links = LinkPaginator(request, name, page)

        data.update(links.adjacent_pages())

        return JsonResponse(data)

    return JsonResponse({})


def books(request):

    data = {'result': [b.to_dict() for b in Book.objects.all()]}

    return JsonResponse(data)
