'''
Created on Jan 27, 2011

@author: Fury
'''
from django.conf.global_settings import DATABASES

''' The Scoring Algorithm v0
add value (+ or -) for each unique found keyword (i.e. if instr > 0)
add geo value if within geo radius
add foursquare value
subtract age penalty for each hour
rank by score and display top 10
'''
import MySQLdb
import tweepy
from tweepy import SearchResult
from django.conf import settings
from MySQLdb import cursors
import warnings
from models import Result
   
def score(object, SearchTerm_id):
    '''TO DO HERE:
    1. make placeholders for rest of scoring algo
    2. make table temporary and unique -- handle multiple simultaneous requests
    3. get results in result object
    4. sort results based on score and truncate to top 10
    '''
    warnings.filterwarnings("ignore", "No data .*")
    
    # try/catch in here at some point
    try:
        db = MySQLdb.connect(settings.DATABASES['default']['HOST'],settings.DATABASES['default']['USER'],settings.DATABASES['default']['PASSWORD'],settings.DATABASES['default']['NAME'])
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])    
    cursor = db.cursor()
    #sql = """DROP TABLE IF EXISTS t_scoring"""
    #cursor.execute(sql)
    #db.commit()
    sql = """CREATE TEMPORARY TABLE t_scoring (
            statusid char(128),
            score INT DEFAULT 0,
            text CHAR(200),
            geo_lat FLOAT,
            geo_lon FLOAT,
            user_name CHAR(50),
            image_url CHAR(250),
            status_date DATETIME,
            SearchTermID INT
            )"""
    cursor.execute(sql)
    db.commit()
    #cursor = db.cursor()   
    for x in object:
        # make sure object is a collection of tweets?
        sql = """
              INSERT INTO t_scoring (statusid, score, text, geo_lat, geo_lon, user_name, image_url, status_date, SearchTermID) 
              VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            cursor.execute (sql, [str(x.id), 50, x.text.encode('utf-8','ingore'), 0, 0, x.from_user, x.profile_image_url, x.created_at, SearchTerm_id])
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        db.commit()
    # run keyword and time penalty parts of scoring proc?
    sql = """CALL sp_ScoreSearchTerm(%s)"""
    try:
        #also try cursor.callproc(procname, args) for less hardcoding
        cursor.execute(sql,SearchTerm_id)
    except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
    db.commit()
    # retrieve data from temp table into object
    # assume re-ranking already done in SQL, so just need to take top 10 rows
    sql = """SELECT * from t_scoring ORDER BY score desc, status_date desc LIMIT 0,10"""
    try:
        cursor.execute(sql)
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
    r = cursor.fetchall()
    retval = {}
    for i in range(cursor.rowcount):
        retval[i] = Result()
        retval[i].statusid      = r[i][0]
        retval[i].score         = r[i][1]
        retval[i].text          = r[i][2]
        retval[i].geo_lat       = r[i][3]
        retval[i].geo_lon       = r[i][4]
        retval[i].from_user     = r[i][5]
        retval[i].profile_image_url     = r[i][6]
        retval[i].created_at    = r[i][7]
        retval[i].SearchTermID  = r[i][8]
    
    # sql = """DROP TABLE IF EXISTS t_scoring"""
    # cursor.execute(sql)  
    
    cursor.close()  
    db.close()
    return retval