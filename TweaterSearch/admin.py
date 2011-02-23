'''
Created on Jan 26, 2011

@author: Fury
'''
from TweaterSearch.models import SearchTerm, Keyword
from django.contrib import admin

class SearchTermAdmin(admin.ModelAdmin):
    fieldsets = [
                 ('Search Info', {'fields': ['phrase', 'friendly_name','pagesize','lang','age_penalty']}),
                 ('Geocode', {'fields': ['use_geo','geo_value', 'geo_dist', 'geocode_lat','geocode_lon',], 'classes': ['collapse']}),
                 ('Foursquare', {'fields': ['use_foursquare','foursquare_val', 'foursquare'], 'classes': ['collapse']}),
                 ('Other Info', {'fields': ['phone','website','address_street1','address_street2','address_city','address_state','address_country','address_zip'], 'classes': ['collapse']})
    ]
admin.site.register(SearchTerm, SearchTermAdmin)
admin.site.register(Keyword)    