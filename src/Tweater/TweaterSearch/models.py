from django.db import models

# Create your models here.
# searchterm needs to be made more friendly for nulls in geo and phone fields
class SearchTerm(models.Model):
    id              = models.AutoField(primary_key=True)
    phrase          = models.CharField("search phrase", max_length=30)
    friendly_name   = models.CharField("friendly name", max_length=50, blank=True)
    pagesize        = models.IntegerField(default='10')
    lang            = models.CharField(max_length=2, default='en')
    geocode_lat     = models.FloatField(null=True)
    geocode_lon     = models.FloatField(null=True)
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
    website         = models.URLField(blank=True)
    phone           = models.CharField(max_length=20)
    def __unicode__(self):
        return self.phrase
    
class Keyword(models.Model):
    id              = models.AutoField(primary_key=True)
    SearchTermID    = models.ForeignKey('SearchTerm')
    phrase          = models.CharField("keyword", max_length=20)
    value           = models.IntegerField(default='10')
    def __unicode__(self):
        return self.phrase + '--' + self.SearchTermID.get_attname()

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