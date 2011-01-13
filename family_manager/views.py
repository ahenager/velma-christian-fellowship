from django.template.context import RequestContext
from django.shortcuts import render_to_response
from models import Family
from vcf.util.search import SearchableBrowse
from django.contrib.auth.decorators import login_required

@login_required
def search(request):

    family_fetch = Family.objects.all().order_by("indexed_name")
    browse_helper = \
        SearchableBrowse(request, family_fetch, ['indexed_name', 'address1', 'address2', 'city', 'state', 'zip', ])
    
    return render_to_response('family_manager/search.html',
                              { 'search_string': browse_helper.search_string,
                                'family_list': browse_helper.result_list},
                              context_instance=RequestContext(request))