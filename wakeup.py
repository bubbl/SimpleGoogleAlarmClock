#!/usr/bin/env python
#
# Simple Google Calendar Alarm Clock
#
# Author: Bart Bania
#
# Website: http://www.bartbania.com
#
import gdata.calendar.service as GServ            #for connection with GCalendar
import time
import os
import random                                     #to play the mp3 later
from ConfigParser import SafeConfigParser
from feed.date.rfc3339 import tf_from_timestamp   #also for the comparator
from datetime import datetime, timedelta          #for the time on the rpi end
from apscheduler.scheduler import Scheduler       #this will let us check the calender on a regular interval
#import logging                                   # used for development. Not needed for normal usage.
#logging.basicConfig(filename='wakeup.log', filemode='w')

parser = SafeConfigParser()                       # initiate Parser and read the configuration file
parser.read('wakeup.cfg')

#************************************************************************************# 
#****           Global variables that can be changed in wakeup.cfg file          ****#
#************************************************************************************# 
email = parser.get('google_credentials', 'email')
password = parser.get('google_credentials', 'password')
q = parser.get('alarm_clock', 'query')
mp3_path = parser.get('alarm_clock', 'mp3_path')

date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
endDate = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

#************************************************************************************# 
#****           Login credentials for your Google Account                        ****#
#************************************************************************************# 
calendar_service = GServ.CalendarService()
calendar_service.email = email
calendar_service.password = password
calendar_service.source = 'SimpleGoogleAlarmClock'
calendar_service.ProgrammaticLogin()
 
#************************************************************************************# 
#****           Main query                                                       ****#
#************************************************************************************# 
def FullTextQuery(calendar_service):
    print 'Full text query for events on Primary Calendar: \'%s\'' % (q)
    query = GServ.CalendarEventQuery('default', 'private', 'full', q)
    query.start_min = date       #  calling date to set the beginning of query range for the present day
    query.start_max = endDate    #  calling endDate to limit the query range to the next 14 days. change tmedelta(days) to set the range
    query.singleevents = 'true'  #  enables creation of repeating events
    query.orderBy = 'startTime'  #  sort by event start time
    query.sortorder = 'a'        #  sort order: ascending
    feed = calendar_service.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
        for a_when in an_event.when:
            print " "
            print an_event.title.text ,"Scheduled:",i,"For:",time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))),"Current Time:",time.strftime('%d-%m-%Y %H:%M')
            if time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))) == time.strftime('%d-%m-%Y %H:%M'):
                print "Waking you up!"
                print "---" 
                songfile = random.choice(os.listdir(mp3_path)) #  choosing by random an .mp3 file from direcotry
                print "Now Playing:", songfile
                                                               #  plays the MP3 in it's entierty. As long as the file is longer 
                                                               #  than a minute it will only be played once:
                command ="mpg321" + " " + mp3_path + "'"+songfile+"'"+ " -g 100" 
                print command
                os.system(command)                             #  plays the song
            else:
                print "Wait for it..."                         #  the event's start time is not the system's current time
 
#************************************************************************************# 
#****           Function to be run by Scheduler                                  ****#
#****           The prints are more for debug than acrual necessity              ****#
#************************************************************************************# 
def callable_func():
    os.system("clear")
    print "----------------------------"
    FullTextQuery(calendar_service)
    print "----------------------------"

#************************************************************************************# 
#****           Run scheduler service                                            ****#
#************************************************************************************# 
sched = Scheduler(standalone=True)
sched.add_interval_job(callable_func,seconds=10)  #  define refresh rate. Set to every 10 seconds by default
sched.start()                                     #  runs the program indefinatly on an interval of x seconds
