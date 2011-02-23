# Create your views here.
from django.core.context_processors import csrf
#from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from smj_app.models import *
from django.forms.models import modelformset_factory
import scoring
import auth


def index(request):
    latest_search_list = SearchTerm.objects.all().order_by('phrase')
    return render_to_response('smj_app/index.html', {'latest_search_list': latest_search_list})

def search(request, SearchTerm_id):
    #need to tidy up variable names
    api = auth.GetTweepyAPI()
    term = get_object_or_404(SearchTerm, id=SearchTerm_id)
    
    recent = api.search(q=term.phrase,lang=term.lang,rpp=term.pagesize)
    '''
    if, for whatever reason, I wanted to return yet more tweets
    i = 2
    while len(recent) < term.pagesize: 
        #of course, pagesize is not the variable here, we don't have a variable for this yet
        #this is wrong in several ways.  Actually, only two ways
        #1: if the number of tweets cached by twitter is less than pagesize, catch and escape that
        #2: once I have enough tweets, chop off the extra ones (currently adds a full page at a time)
        recent.extend(api.search(q=term.phrase,lang=term.lang,page=i))
        i += 1
    '''    
        
    r = scoring.score(recent, SearchTerm_id)
    template = 'smj_app/results.html'
    return render_to_response( template , {'results': r.values(), 'term': term.phrase}, context_instance = RequestContext( request ))

def rawsearch(request, SearchTerm_id):
    api = auth.GetTweepyAPI()
    if request.method == 'POST':
        recent = api.search(q=request.POST["q"],lang="en")
    else:
        term = SearchTerm.objects.get(id=SearchTerm_id)
        recent = api.search(q=term.phrase,lang=term.lang)       
    #leave at default number of results, or perhaps more vs. page limit for variety  
    template = 'smj_app/results.html'
    return render_to_response( template , {'results': recent }, context_instance = RequestContext( request ))       

def termadmin(request, SearchTerm_id):
    template = 'smj_app/term_admin.html'
    data = {'id' : SearchTerm_id }
    return render_to_response( template , data, context_instance = RequestContext( request ))

def termform(request, SearchTerm_id):
    template = 'smj_app/termform.html'  
    if request.method == 'POST':
        if SearchTerm_id == '0':
            f = SearchTermFormAll(request.POST)
        #add yet more validation here. eventually.
        else: 
            t = SearchTerm.objects.get(pk=SearchTerm_id)
            f = SearchTermFormAll(request.POST, instance=t)
        if f.is_valid():
            f.save()
    else:
        #if the request is not a post, i.e. you are just retrieving the existing list
        t = SearchTerm.objects.get(pk=SearchTerm_id)
        f = SearchTermFormAll(instance=t)
    data = { 'form': f, 'id' : SearchTerm_id }
    return render_to_response( template , data, context_instance = RequestContext( request ))


def edit(request, SearchTerm_id):
    #render current list of keywords/weights
    template = 'smj_app/termdetail.html'
    return render_to_response( template , {'SearchTermID': SearchTerm_id}, context_instance = RequestContext( request ))

def keywordformsetfactory(request, SearchTerm_id):  
    KeywordFormset = modelformset_factory(Keyword, KeywordForm, can_delete=1, extra=0, max_num = None)
    #put some validation here..
    if request.method == 'POST':
        #add yet more validation here. eventually.
            formset = KeywordFormset(request.POST, request.FILES)        
            if not formset.is_valid():
                print formset.errors
                pass
            else:
                formset.save()
    else:
        #if the request is not a post, i.e. you are just retrieving the existing list
        formset = KeywordFormset(queryset = Keyword.objects.filter(SearchTermID=SearchTerm_id))
    template = 'smj_app/keywordform.html'
    return render_to_response(template, {'formset' : formset, 'SearchTermID' : SearchTerm_id}, context_instance = RequestContext( request ))

def neworedit(request, SearchTerm_id):     
    if SearchTerm_id == '0':
        t = SearchTerm
        f = SearchTermFormAll()
        template = 'smj_app/termform.html'
        data = { 'form': f, 'id' : 0 }
    else:
        t = SearchTerm.objects.get(pk=SearchTerm_id)   
        template = 'smj_app/termform.html'
        #if the request is not a post, i.e. you are just retrieving the existing list
        f = SearchTermFormAll(instance=t)
        data = { 'form': f, 'id' : SearchTerm_id }
    return render_to_response( template , data, context_instance = RequestContext( request ))     

def delkw(request, kid, SearchTerm_id):
    #render current list of keywords/weights
    if Keyword.objects.filter(SearchTermID=SearchTerm_id).count() > 1:
        k = Keyword.objects.get(id=kid)
        k.delete()
    else:
        #print "SearchTerm must have at least one Keyword"
        raise Exception("SearchTerm must have at least one Keyword")
    template = 'smj_app/keywordform.html'
    KeywordFormset = modelformset_factory(Keyword, can_delete=1, extra=0, max_num = None)
    formset = KeywordFormset(queryset = Keyword.objects.filter(SearchTermID=SearchTerm_id))
    return render_to_response(template, {'formset' : formset, 'SearchTermID' : SearchTerm_id}, context_instance = RequestContext( request ))

def delst(request, SearchTerm_id):
    term = get_object_or_404(SearchTerm, id=SearchTerm_id)
    term.delete()
    latest_search_list = SearchTerm.objects.all().order_by('phrase')
    return render_to_response('smj_app/index.html', {'latest_search_list': latest_search_list})

def addtodo(request):
    if request.method == 'POST':
        f = TodoFormAdd(request.POST)
        if f.is_valid():
            f.save()
    else:
            f = TodoFormAdd()
    template = 'smj_app/addtodo.html'  
    data = { 'form': f, 'id' : 0 }
    return render_to_response( template , data, context_instance = RequestContext( request ))

def managetodo(request):  
    TodoFormset = modelformset_factory(Todo, TodoFormEdit, can_delete=1, extra=0, max_num = None)
    #put some validation here..
    if request.method == 'POST':
        #add yet more validation here. eventually.
            formset = TodoFormset(request.POST, request.FILES)        
            if not formset.is_valid():
                print formset.errors
                pass
            else:
                formset.save()
    else:
        #if the request is not a post, i.e. you are just retrieving the existing list
        formset = TodoFormset()
    template = 'smj_app/todo.html'
    return render_to_response(template, {'formset' : formset}, context_instance = RequestContext( request ))

def viewtodo(request):  
    todolist = Todo.objects.all()
    #should probably exclude completed/rejected tasks, or provide filter in view
    template = 'smj_app/todolist.html'
    return render_to_response(template, {'todolist' : todolist}, context_instance = RequestContext( request ))

def about(request):
    template = 'smj_app/about.html'
    return render_to_response(template, context_instance = RequestContext( request ))

def contact(request):
    template = 'smj_app/contact.html'
    return render_to_response(template, context_instance = RequestContext( request ))
