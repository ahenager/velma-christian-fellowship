import re
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage

class SearchableBrowse:
    RESULTS_PER_PAGE = 10

    def normalize_query(self, query_string,
                        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                        normspace=re.compile(r'\s{2,}').sub):
        ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
            and grouping quoted words together.
            Example:

            >>> normalize_query('  some random  words "with   quotes  " and   spaces')
            ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

        '''
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

    def get_query(self, query_string, search_fields):
        ''' Returns a query, that is a combination of Q objects. That combination
            aims to search keywords within a model by testing the given search fields.

        '''
        query = None # Query to search for every search term
        terms = self.normalize_query(query_string)
        for term in terms:
            or_query = None # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    def __init__(self, request, source_query_set, search_fields, results_per_page=RESULTS_PER_PAGE):
        self.search_string = ""
        if ('q' in request.GET) and request.GET['q'].strip():
            self.search_string = request.GET['q']

            entry_query = self.get_query(self.search_string, search_fields)

            source_query_set = source_query_set.filter(entry_query)

        paginator = Paginator(source_query_set, results_per_page)

        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            self.result_list = paginator.page(page)
        except (EmptyPage, InvalidPage):
            self.result_list = paginator.page(paginator.num_pages)