#!/usr/bin/env python
#These are the imports google said to include
import gdata.calendar
import gdata.calendar.service
import gdata.service
import atom.service
import atom
import getopt
import sys
import string
import time
 
import xe #for the time comparator
from feed.date.rfc3339 import tf_from_timestamp #also for the comparator
from datetime import datetime, timedelta #for the time on the rpi end
from apscheduler.scheduler import Scheduler #this will let us check the calender on a regular interval
import os, random #to play the mp3 later
import logging

logging.basicConfig()
 
# Login credentials
calendar_service = gdata.calendar.service.CalendarService()
calendar_service.email = '***@gmail.com' #your email
calendar_service.password = '***' #your password
calendar_service.source = 'SimpleGoogleAlarmClock'
calendar_service.ProgrammaticLogin()

def FullTextQuery(calendar_service, text_query='wake'):
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    endDate = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    print 'Full text query for events on Primary Calendar: \'%s\'' % ( text_query,)
    query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full', text_query)
    query.timeMin = date
    query.timeMax = endDate
    query.ctz = 'Europe/London'
    query.singleevents = 'true'
    query.orderBy = 'startTime'
    query.max_results = '10'
    feed = calendar_service.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
        for a_when in an_event.when:
            print " "
            print an_event.title.text ,"Scheduled:",i,"For:",time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))),"Current Time:",time.strftime('%d-%m-%Y %H:%M')
 
            if time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))) == time.strftime('%d-%m-%Y %H:%M'):
                print "Waking you up!"
                print "---"
 
                songfile = random.choice(os.listdir("/home/pi/mp3/")) #chooses the .mp3 file
                print "Now Playing:", songfile
                command ="mpg321" + " " + "/home/pi/mp3/" + "'"+songfile+"'"+ " -g 100" #plays the MP3 in it's entierty. As long as the song is longer than a minute then will only trigger once in the minute that start of the "wake" event
 
                print command
                os.system(command) #runs the bash command
            else:
                print "Wait for it..." #the "wake" event's start time != the system's current time
 
def callable_func():
    os.system("clear") #this is more for my benefit and is in no way necesarry
    print "----------------------------"
    FullTextQuery(calendar_service)
    print "----------------------------"
 
scheduler = Scheduler(standalone=True)
scheduler.add_interval_job(callable_func,seconds=10)
scheduler.start() #runs the program indefinatly on an interval of 5 seconds
