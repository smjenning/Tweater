from django.db import models
from django.forms import ModelForm, Textarea
from django.forms.models import modelformset_factory
from django import forms
from django.contrib.auth.models import User
import datetime


# Create your models here.
# searchterm needs to be made more friendly for nulls in geo and phone fields
class SearchTerm(models.Model):
    id              = models.AutoField(primary_key=True)
    phrase          = models.CharField("search phrase", max_length=30, unique=True)
    friendly_name   = models.CharField("friendly name", max_length=50, blank=True)
    pagesize        = models.IntegerField(default='10')
    lang            = models.CharField(max_length=2, default='en')
    geocode_lat     = models.FloatField(null=True, default='0')
    geocode_lon     = models.FloatField(null=True, default='0')
    use_geo         = models.BooleanField(default=False)
    geo_value       = models.IntegerField(default='5')
    geo_dist        = models.IntegerField(default='1') #radius distance in km
    foursquare      = models.CharField("foursquare ID", max_length=128, blank=True) #actual data type & how we get it TBD
    use_foursquare  = models.BooleanField(default=False)
    foursquare_val  = models.IntegerField(default='20')
    age_penalty     = models.IntegerField(default='5')
    address_street1 = models.CharField(max_length=50, blank=True)
    address_street2 = models.CharField(max_length=50, blank=True)
    address_city    = models.CharField(max_length=50, blank=True)
    address_state   = models.CharField(max_length=50, blank=True)
    address_country = models.CharField(max_length=50, blank=True)
    address_zip     = models.CharField(max_length=50, blank=True)
    website         = models.URLField(blank=True, default='www.google.com')
    phone           = models.CharField(max_length=20,default='0')
    createdby       = models.ForeignKey(User, blank=True, null=True)
    createddate     = models.DateTimeField(default=datetime.datetime.now())
    def __unicode__(self):
        return self.phrase
    def save(self, *args, **kwargs):
        if self.pk:
            super(SearchTerm, self).save(*args, **kwargs)
        else:
            super(SearchTerm, self).save(*args, **kwargs)
            k = Keyword()
            k.phrase = self.phrase
            k.SearchTermID = self
            k.score = 10
            k.save() 
   
class Keyword(models.Model):
    id              = models.AutoField(primary_key=True)
    SearchTermID    = models.ForeignKey('SearchTerm')
    phrase          = models.CharField("keyword", max_length=20)
    value           = models.IntegerField(default='10')
    def __unicode__(self):
        return self.phrase + '--'# + self.SearchTermID.get_attname()

class Result(models.Model):
    statusid        = models.IntegerField(default='0')
    score           = models.IntegerField(default='0')
    text            = models.CharField(max_length=200, blank=True)
    geo_lat         = models.IntegerField(default='0')
    geo_lon         = models.IntegerField(default='0')
    from_user       = models.CharField(max_length=200, blank=True)
    profile_image_url = models.CharField(max_length=200, blank=True)
    created_at      = models.DateTimeField(blank=True)
    SearchTermID    = models.IntegerField(default='0')
    def __unicode__(self):
        return self.statusid + '--' + self.from_user

class Todo(models.Model):
    TYPE_CHOICES    = (
                       ('B','bug'),
                       ('E','enhancement'),
                       )
    STATUS_CHOICES  = (
                       ('S','submitted'),
                       ('R','rejected'),
                       ('A','accepted'),
                       ('P','in progress'),
                       ('D','done'),
                       )
    id              = models.AutoField(primary_key=True)
    createdby       = models.ForeignKey(User, blank=True, null=True)
    createddate     = models.DateTimeField(default=datetime.datetime.now())
    summary         = models.CharField(max_length=200, blank=True)
    action          = models.CharField(max_length=200, blank=True)
    type            = models.CharField(max_length=1, choices=TYPE_CHOICES, default='B')
    status          = models.CharField(max_length=1, choices=STATUS_CHOICES, default='S')
    def __unicode__(self):
        return self.summary
    
class SearchTermForm(ModelForm):
    class Meta:
        model = SearchTerm
        fields = ('id','phrase', 'use_geo', 'geocode_lat', 'geocode_lon')
        
class SearchTermFormAll(ModelForm):
    class Meta:
        model = SearchTerm

class KeywordForm(ModelForm): 
    #phrase = forms.TextInput({'size': '5'})
    #score = forms.CharField(widget=forms.Textarea(attrs={'cols': '5'}))
    #id = forms.ModelChoiceField(queryset=SearchTerm.objects.all())
    def __init__(self, *args, **kwargs):
        super(KeywordForm, self).__init__(*args, **kwargs)
        self.fields['phrase'].widget.attrs['size'] = '20'
        self.fields['value'].widget.attrs['size'] = '5'
    class Meta:
        model = Keyword
        fields = ('SearchTermID','phrase','value')

class TodoFormAdd(ModelForm): 
    def __init__(self, *args, **kwargs):
        super(TodoFormAdd, self).__init__(*args, **kwargs)
    class Meta:
        model = Todo
        fields = ('summary','type')
        widgets = {'summary': 
                   Textarea(attrs={'cols': 30, 'rows': 3})
                   }
       
class TodoFormEdit(ModelForm): 
    def __init__(self, *args, **kwargs):
        super(TodoFormEdit, self).__init__(*args, **kwargs)
    class Meta:
        model = Todo
        widgets = {'summary': 
                   Textarea(attrs={'cols': 30, 'rows': 3}),
                   'action': 
                   Textarea(attrs={'cols': 30, 'rows': 3}),
                   }

    