'''
@author eagapie
contains the views related to the medicloud app
'''

from django.http       import HttpResponse, HttpResponseRedirect
from django.template   import Context, loader, RequestContext
from django.shortcuts  import render, get_object_or_404, render_to_response
from django            import forms
from mediacloud.models import Media, Story, MediaCategory, Companies
from mediacloud.forms  import SearchForm
from wikileaks.models  import Wikileaks


def index(request):
    latest_media_id_list = Media.objects.order_by('media_id')[:20]
    context = {'media_id_list' : latest_media_id_list}
    return render(request, 'mediacloud/index.html', context)


# the details of the media source
def detail_media(request, media_id):
    media = get_object_or_404(Media, media_id=media_id)
    return render(request, 'mediacloud/detail_media.html', {'media': media})


# the details of the stories
def detail_story(request, story_id):
    story = get_object_or_404(Story, story_id=story_id)
    return render(request, 'mediacloud/detail_story.html', {'story': story})


# this builds the information for the search form
def search_cat(request):

    # when the post parameters are submitted
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            #  the form returns a list  of the id of the category
            post_categ = request.POST.getlist('category')[0]
            post_comp  = request.POST.getlist('company')[0]
# this code will be uncommented with the form filed that corresponds to this and will assist in selectively adding the company in the search or not
#            post_useComp = request.POST.getlist('includeCompany')[0]
            
            # get the appropriate cateogy, comapnies and media objects
            categ_obj  = MediaCategory.objects.get(id = post_categ)
            comp_obj   = Companies.objects.get(id = post_comp)
            # all media sources that have the same category
            media_list = Media.objects.filter(category = categ_obj.category) 

            # get the stories correcponding to the media id
            # from the stories returned select only the ones that contain the company name
            all_story = []
            for it_media in media_list:
                story_list = Story.objects.filter(media = it_media )

# this commented part of the code does the search by company, it should be commented back on                
#                if post_useComp is None:
#                    print 'we got it'
#                    for it_story in story_list:
#                        print it_story.companies
#                        if all_story is not None:
#                            all_story.append(it_story)
#                        else:
#                            all_story = [it_story]
#                else:
                all_story.extend(story_list)

            # get the wikileaks information          
            categ_obj=Companies.objects.get(id=post_comp)
            query = categ_obj.name

            wikileaks_sales_withlobbying = Wikileaks.objects.filter(Company__iexact=query,Rating=4).order_by('-Sales')
            wikileaks_litigation_withlobbying = Wikileaks.objects.filter(Company__iexact=query,Rating=4).order_by('-Litigation')
            wikileaks_competitor_withlobbying = Wikileaks.objects.filter(Company__iexact=query,Rating=4).order_by('-Competitor')
            wikileaks_sales = Wikileaks.objects.filter(Company__iexact=query).order_by('-Sales')
            wikileaks_litigation = Wikileaks.objects.filter(Company__iexact=query).order_by('-Litigation')
            wikileaks_competitor = Wikileaks.objects.filter(Company__iexact=query).order_by('-Competitor')
#
#            return render(request, 'wikileaks/search_results.html', {'wikileaks_sales_withlobbying': wikileaks_sales_withlobbying, 'wikileaks_litigation_withlobbying': wikileaks_litigation_withlobbying, 'wikileaks_competitor_withlobbying': wikileaks_competitor_withlobbying,'wikileaks_sales': wikileaks_sales, 'wikileaks_litigation': wikileaks_litigation, 'wikileaks_competitor': wikileaks_competitor, 'query': categ_obj})

            var = {'media_list' : media_list, 'story_list' : all_story, 'category' : post_categ, \
                'wikileaks_sales_withlobbying': wikileaks_sales_withlobbying, 'wikileaks_litigation_withlobbying': wikileaks_litigation_withlobbying, 'wikileaks_competitor_withlobbying': wikileaks_competitor_withlobbying,'wikileaks_sales': wikileaks_sales, 'wikileaks_litigation': wikileaks_litigation, 'wikileaks_competitor': wikileaks_competitor, 'query': categ_obj}

            return render(request, 'mediacloud/search_cat_results.html', var)
    # when the post parameters were not submitted yet
    else:
        form = SearchForm()

    return render_to_response('mediacloud/search_cat.html', {'search_cat_form': form}, context_instance=RequestContext(request))


# renders the template with the results of the search query
def search_cat_results(request):
    return render_to_response('mediacloud/search_cat_results.html')

def search_results_wikileaks(request):
    return render_to_response('wikileaks/search_results.html')
