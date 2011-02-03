# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from Tweater.TweaterSearch.models import SearchTerm, Result
import httplib, time, datetime
import tweepy
import scoring
from django.template.context import RequestContext

def index(request):
    latest_search_list = SearchTerm.objects.all().order_by('phrase')[:5]
    return render_to_response('TweaterSearch/index.html', {'latest_search_list': latest_search_list})

def search(request, SearchTerm_id):
    #need to tidy up variable names
    #should probably encapsulate the below in a separate function, call it, and return the API object

    CKEY = 'txYyE7H7C0pVyaYFsxO2Zw'
    CSEC = 'vB9JB5LPLSeaA5Dw6bkAEJ0ACSxTkyDgG2lqUfEh0'
    key = '54029241-JhgcPE60C4qYbxLasXItdMkznEVvaGvTdTCPKBlkL'
    secret = 'pOrN1KST5PGZgkvWmQrSGtWymAflU0BL1VLYv1ZIw'
    auth = tweepy.OAuthHandler(CKEY,CSEC)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    term = SearchTerm.objects.get(id=SearchTerm_id)
    recent = api.search(q=term.phrase,lang=term.lang)
    #need to get more results until page_size limit is reached
    r = scoring.score(recent, SearchTerm_id)
    template = 'TweaterSearch/results.html'
    #return render_to_response('TweaterSearch/search.html', {'r': r.values(), 'term': term.phrase})
    return render_to_response( template , {'results': r.values(), 'term': term.phrase}, context_instance = RequestContext( request ))

def rawsearch(request, SearchTerm_id):
    #need to tidy up variable names
    #should probably encapsulate the below in a separate function, call it, and return the API object

    CKEY = 'txYyE7H7C0pVyaYFsxO2Zw'
    CSEC = 'vB9JB5LPLSeaA5Dw6bkAEJ0ACSxTkyDgG2lqUfEh0'
    key = '54029241-JhgcPE60C4qYbxLasXItdMkznEVvaGvTdTCPKBlkL'
    secret = 'pOrN1KST5PGZgkvWmQrSGtWymAflU0BL1VLYv1ZIw'
    auth = tweepy.OAuthHandler(CKEY,CSEC)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    term = SearchTerm.objects.get(id=SearchTerm_id)
    recent = api.search(q=term.phrase,lang=term.lang)
    #need to get more results until page_size limit is reached
    
    template = 'TweaterSearch/results.html'
    return render_to_response( template , {'results': recent, 'term': term.phrase}, context_instance = RequestContext( request ))
        
       

def termadmin(request):
    template = 'TweaterSearch/term_admin.html'
    data = {}
    #return render_to_response('TweaterSearch/term_admin.html', {'result': r.values(), 'phrase': term.phrase})
    return render_to_response( template , data, context_instance = RequestContext( request ))

def edit(request, SearchTerm_id):
    #idea is to render current list of keywords/weights
    #submit field for new keywords, or direct editing of existing (auto-refresh on change)
    #on another tab/area of the form, be able to change further details on search term
    #so, right now passing just the term ID...
    template = 'TweaterSearch/termdetail.html'
    return render_to_response( template , {'SearchTermID': SearchTerm_id}, context_instance = RequestContext( request ))
