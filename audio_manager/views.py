from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from models import AudioMedia, Category
from django.shortcuts import render_to_response
from vcf.util.search import SearchableBrowse

@login_required
def search(request):
    try:
        category = int(request.GET.get('category', 0))
    except ValueError:
        category = None

    if category > 0 and category is not None:
        audio_fetch = AudioMedia.objects.filter(categories__id=category).order_by("name")
    else:
        audio_fetch = AudioMedia.objects.all().order_by("name")


    browse_helper = SearchableBrowse(request, audio_fetch, ['name', 'description', ])

    category_list = Category.objects.all().order_by('name')

    return render_to_response('audio_manager/search.html',
                              { 'search_string': browse_helper.search_string,
                                'audio_list': browse_helper.result_list,
                                'category_list' : category_list,
                                'category' : category},
                              context_instance=RequestContext(request))
