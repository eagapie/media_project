from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from wikileaks.models import Wikileaks
from mediacloud.models import Story

def index(request):
    latest_wikileaks_list = Wikileaks.objects.filter(Rating='4').order_by('-Sales')[:40]
    latest_wikileaks_litigation_list = Wikileaks.objects.filter(Rating='4').order_by('-Litigation')[:40]
    latest_wikileaks_competitor_list = Wikileaks.objects.filter(Rating='4').order_by('-Competitor')[:40]
    t =  loader.get_template('wikileaks/index.html')
    c = Context({
        'latest_wikileaks_list': latest_wikileaks_list,
        'latest_wikileaks_litigation_list': latest_wikileaks_litigation_list,
	'latest_wikileaks_competitor_list': latest_wikileaks_competitor_list,
    })
    return HttpResponse(t.render(c))

def detail(request, wikileaks_id):
    p = get_object_or_404(Wikileaks, id=wikileaks_id)
    return render_to_response('wikileaks/detail.html', {'wikileaks': p})

def search_form(request):
    return render_to_response('wikileaks/search_form.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
	q = request.GET['q']
	wikileaks_sales_withlobbying = Wikileaks.objects.filter(Company__iexact=q,Rating=4).order_by('-Sales')
	wikileaks_litigation_withlobbying = Wikileaks.objects.filter(Company__iexact=q,Rating=4).order_by('-Litigation')
	wikileaks_competitor_withlobbying = Wikileaks.objects.filter(Company__iexact=q,Rating=4).order_by('-Competitor')
	wikileaks_sales = Wikileaks.objects.filter(Company__iexact=q).order_by('-Sales')
        wikileaks_litigation = Wikileaks.objects.filter(Company__iexact=q).order_by('-Litigation')
        wikileaks_competitor = Wikileaks.objects.filter(Company__iexact=q).order_by('-Competitor')
	return render_to_response('wikileaks/search_results.html',
	    {'wikileaks_sales_withlobbying': wikileaks_sales_withlobbying, 'wikileaks_litigation_withlobbying': wikileaks_litigation_withlobbying, 'wikileaks_competitor_withlobbying': wikileaks_competitor_withlobbying,'wikileaks_sales': wikileaks_sales, 'wikileaks_litigation': wikileaks_litigation, 'wikileaks_competitor': wikileaks_competitor, 'query': q})
    else:
	return HttpResponse('Please submit a search term.')
#    if 'q' in HttpRequest.get_full_path() and HttpRequest.get_full_path('q')
#	q = HttpRequest.get_full_path('q')
#	wikileaks = Wikileaks.objects.filter(Cable_icontains=q)
#	return render_to_response('wikileaks/search_results.html',
#	    {'wikileaks': wikileaks, 'query': q})
#    else:
#	return HttpResponse('Please submit a search term.')
