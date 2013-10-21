#!/usr/bin/env python
#
# Simple Google Calendar Alarm Clock
#
# Author: Bart Bania
#
# Website: http://www.bartbania.com
#
import gdata.calendar.service as GServ 
import gdata.service
import gdata.calendar # for connection with GCalendar
import time
from ConfigParser import SafeConfigParser
import os, random #to play the mp3 later
 
from feed.date.rfc3339 import tf_from_timestamp #also for the comparator
from datetime import datetime, timedelta #for the time on the rpi end
from apscheduler.scheduler import Scheduler #this will let us check the calender on a regular interval

#import logging # used for development. Not needed for normal usage.
#logging.basicConfig(filename='log.log', filemode='w')

#************************************************************************************# 
#****           Global variables that can be changed in wakeup.cfg file          ****#
#************************************************************************************# 
global email, password, q, mp3_path
parser = SafeConfigParser()
parser.read('wakeup.cfg')

email = parser.get('google_credentials', 'email')
password = parser.get('google_credentials', 'password')
q = parser.get('alarm_clock', 'query')
mp3_path = parser.get('alarm_clock', 'mp3_path')

#************************************************************************************# 
#****           Login credentials for your Google Account                        ****#
#************************************************************************************# 
calendar_service = GServ.CalendarService()
calendar_service.email = email
calendar_service.password = password
calendar_service.source = 'SimpleGoogleAlarmClock'
calendar_service.ProgrammaticLogin()
 
#************************************************************************************# 
#****           Main querry definition                                           ****#
#************************************************************************************# 
def FullTextQuery(calendar_service):
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    endDate = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    print 'Full text query for events on Primary Calendar: \'%s\'' % (q)
    query = GServ.CalendarEventQuery('default', 'private', 'full', q)
    query.timeMin = date
    query.timeMax = endDate
    query.singleevents = 'true'
    query.orderBy = 'startTime'
    query.sortorder = 'a'
#    query.max_results = '10'
    feed = calendar_service.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
        for a_when in an_event.when:
            print " "
            print an_event.title.text ,"Scheduled:",i,"For:",time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))),"Current Time:",time.strftime('%d-%m-%Y %H:%M')
            if time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))) == time.strftime('%d-%m-%Y %H:%M'):
                print "Waking you up!"
                print "---" 
                songfile = random.choice(os.listdir(mp3_path)) #chooses the .mp3 file
                print "Now Playing:", songfile
                command ="mpg321" + " " + mp3_path + "'"+songfile+"'"+ " -g 100" #plays the MP3 in it's entierty. As long as the song is longer than a minute then will only trigger once in the minute that start of the event
                print command
                os.system(command) #runs the bash command
            else:
                print "Wait for it..." #the event's start time is not the system's current time
 
def callable_func():
    os.system("clear") #this is more for my benefit and is in no way necesarry
    print "----------------------------"
    FullTextQuery(calendar_service)
    print "----------------------------"

sched = Scheduler(standalone=True)
sched.add_interval_job(callable_func,seconds=10)
sched.start() #runs the program indefinatly on an interval of x seconds 
