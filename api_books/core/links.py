class LinkPaginator:

    def __init__(self, request, name, page):
        self.name = name
        self.page = page
        self.page_size = page.paginator.per_page
        self.request = request

    def _build_query_string(self, page_number):

        if self.name:
            uri = f'?name={self.name}&page={page_number}&page_size={self.page_size}'
        else:
            uri = f'?page={page_number}&page_size={self.page_size}'

        return uri

    def adjacent_pages(self):

        d = dict()

        if self.page.has_previous():
            page_number = self.page.previous_page_number()
            d['previous'] = self.request.build_absolute_uri(f'/api/authors{self._build_query_string(page_number)}')
        if self.page.has_next():
            page_number = self.page.next_page_number()
            d['next'] = self.request.build_absolute_uri(f'/api/authors{self._build_query_string(page_number)}')

        return d
