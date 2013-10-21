#!/usr/bin/env python
import gdata.calendar.service
import gdata.service
import gdata.calendar
import atom
import atom.service
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

#************************************************************************************# 
#****           Login credentials for your Google Account                        ****#
#************************************************************************************# 

calendar_service = gdata.calendar.service.CalendarService()
calendar_service.email = 'you@gmail.com'
calendar_service.password = '***'
calendar_service.source = 'SimpleGoogleAlarmClock'
calendar_service.ProgrammaticLogin()
 
#************************************************************************************# 
#****           Global variables that can be changed                             ****#
#************************************************************************************# 

q = 'wake' #calendar query
mp3_dir = "/home/pi/mp3/" #mp3 directory

#************************************************************************************# 
#****           Main querry definition                                           ****#
#************************************************************************************# 

def FullTextQuery(calendar_service):
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    endDate = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    print 'Full text query for events on Primary Calendar: \'%s\'' % (q)
    query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full', q)
    query.timeMin = date
    query.timeMax = endDate
#    query.ctz = 'Europe/London'
    query.singleevents = 'true'
    query.orderBy = 'startTime'
    query.sortorder = 'a'
    query.max_results = '10'
    feed = calendar_service.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
        for a_when in an_event.when:
            print " "
            print an_event.title.text ,"Scheduled:",i,"For:",time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))),"Current Time:",time.strftime('%d-%m-%Y %H:%M')
            if time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))) == time.strftime('%d-%m-%Y %H:%M'):
                print "Waking you up!"
                print "---" 
                songfile = random.choice(os.listdir(mp3_dir)) #chooses the .mp3 file
                print "Now Playing:", songfile
                command ="mpg321" + " " + mp3_dir + "'"+songfile+"'"+ " -g 100" #plays the MP3 in it's entierty. As long as the song is longer than a minute then will only trigger once in the minute that start of the event
                print command
                os.system(command) #runs the bash command
            else:
                print "Wait for it..." #the event's start time is not the system's current time
 
def callable_func():
    os.system("clear") #this is more for my benefit and is in no way necesarry
    print "----------------------------"
    FullTextQuery(calendar_service)
    print "----------------------------"
 
scheduler = Scheduler(standalone=True)
scheduler.add_interval_job(callable_func,seconds=10)
scheduler.start() #runs the program indefinatly on an interval of 10 seconds
