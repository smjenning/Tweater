# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from Tweater.TweaterSearch.models import SearchTerm, Keyword, KeywordForm, SearchTermForm
from django.forms.models import modelformset_factory
import scoring
import auth

def index(request):
    latest_search_list = SearchTerm.objects.all().order_by('phrase')[:5]
    return render_to_response('TweaterSearch/index.html', {'latest_search_list': latest_search_list})

def search(request, SearchTerm_id):
    #need to tidy up variable names
    api = auth.GetTweepyAPI()
    term = SearchTerm.objects.get(id=SearchTerm_id)
    recent = api.search(q=term.phrase,lang=term.lang)
    #need to get more results until page_size limit is reached
    r = scoring.score(recent, SearchTerm_id)
    template = 'TweaterSearch/results.html'
    return render_to_response( template , {'results': r.values(), 'term': term.phrase}, context_instance = RequestContext( request ))

def rawsearch(request, SearchTerm_id):
    api = auth.GetTweepyAPI()
    if request.method == 'POST':
        #if SearchTerm_id == 0:
        recent = api.search(q=request.POST["q"],lang="en")
        #recent = api.search(q=request.POST['q'],lang="en")
        #else:
        #    term = SearchTerm.objects.get(id=SearchTerm_id)
        #    recent = api.search(q=term.phrase,lang=term.lang)
    else:
        term = SearchTerm.objects.get(id=SearchTerm_id)
        recent = api.search(q=term.phrase,lang=term.lang)
    #leave at default number of results, or perhaps more vs. page limit for variety  
    template = 'TweaterSearch/results.html'
    return render_to_response( template , {'results': recent }, context_instance = RequestContext( request ))       

def termadmin(request, SearchTerm_id):
    template = 'TweaterSearch/term_admin.html'
    data = {'id' : SearchTerm_id }
    #return render_to_response('TweaterSearch/term_admin.html', {'result': r.values(), 'phrase': term.phrase})
    return render_to_response( template , data, context_instance = RequestContext( request ))

def termform(request, SearchTerm_id):
    template = 'TweaterSearch/termform.html'
    t = SearchTerm.objects.get(pk=SearchTerm_id)   
    if request.method == 'POST':
        #add yet more validation here. eventually.
        f = SearchTermForm(request.POST, instance=t)
        if f.is_valid():
            f.save()
    else:
        #if the request is not a post, i.e. you are just retrieving the existing list
        f = SearchTermForm(instance=t)
    data = { 'form': f, 'id' : SearchTerm_id }
    #return render_to_response('TweaterSearch/term_admin.html', {'result': r.values(), 'phrase': term.phrase})
    return render_to_response( template , data, context_instance = RequestContext( request ))


def edit(request, SearchTerm_id):
    #idea is to render current list of keywords/weights
    #submit field for new keywords, or direct editing of existing (auto-refresh on change)
    #on another tab/area of the form, be able to change further details on search term
    #so, right now passing just the term ID...
    template = 'TweaterSearch/termdetail.html'
    return render_to_response( template , {'SearchTermID': SearchTerm_id}, context_instance = RequestContext( request ))

def keywordformsetfactory(request, SearchTerm_id):
    #KeywordFormset = modelformset_factory(Keyword,KeywordForm,can_delete=True)
    KeywordFormset = modelformset_factory(Keyword, can_delete=1)
    #put some validation here..
    if request.method == 'POST':
        #add yet more validation here. eventually.
            formset = KeywordFormset(request.POST, request.FILES)
            formset.save()
    else:
        #if the request is not a post, i.e. you are just retrieving the existing list
        formset = KeywordFormset(queryset = Keyword.objects.filter(SearchTermID=SearchTerm_id))
        ''' want to find a way to default searchterm fk for unsaved records...
        for form in formset.save(commit=False):
            form.SearchTermID = SearchTerm.objects.get(id=SearchTerm_id)
            form.save()
        formset.save()
        '''
    template = 'TweaterSearch/keywordform.html'
    return render_to_response(template, {'formset' : formset, 'SearchTermID' : SearchTerm_id}, context_instance = RequestContext( request ))
