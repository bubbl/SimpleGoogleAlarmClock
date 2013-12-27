wakeup.py 
===========

An alarm clock that syncs with Google Calendar, written in Python.

#### Features

The alarm dates are read from Google Calendar, any event with the text of your choice will be fetched and alarm triggered from console. 

#### Requirements

It needs the following libraries installed on your Raspberry Pi:

* [Google Data Library](https://developers.google.com/gdata/articles/python_client_lib#linux)
* [APScheduler](http://pythonhosted.org/APScheduler/#installing-apscheduler)
* PyFeed:

can be found in **libs** directory. From the repository dir:

        > cd libs
        > tar -zxvf pyfeed-0.7.4.tar.gz
        > cd pyfeed-0.7.4
        > sudo python setup.py install

* mpg321:

        > sudo apt-get install -y mpg321

NOTE: If you’ve never used sound playback on your Raspberry Pi, head [HERE](http://www.raspberrypi-spy.co.uk/2013/06/raspberry-pi-command-line-audio/) for instructions.

#### How to use it
* Copy (git clone) all provided files into a new directory. 
* Edit the config file **wakeup.cfg** with your Google credentials and mp3 path. 
* If you’re using [2-step verification](http://www.google.com/intl/en-GB/landing/2step/), first you need to generate an [application-specific password](https://support.google.com/accounts/answer/185833). 
* The alarm clock can be started by running the command:

        > python wakeup.py

or to run it in background:

        > nohup python wakeup.py &

* To add alarm at specific time/date, just head to Google Calendar and create an Event with phrase **wake** in the title. The phrase can be easily changed in the config file.

#### The Config file

The Python code doesn't contain any authentication data. I’ve decided to move it to a separate file, as I believe it’s easier for the user to set the variables in a separate place, where no code could be accidentally altered or deleted. The program gets the configuration thanks to ConfigParser that reads the configuration file and passes the variables to the program:

    global email, password, q, mp3_path
    parser = SafeConfigParser()
    parser.read('wakeup.cfg')
    
    email = parser.get('credentials', 'email')
    password = parser.get('credentials', 'password')
    q = parser.get('alarm', 'query')
    mp3_path = parser.get('alarm', 'mp3_path')

The file is has a structure similar to what you would find on Microsoft Windows INI files. The configuration file consists of sections, led by a [section] header and followed by name = value entries. My config file consists of two sections (just my personal preference) one for credentials and the other for event query and mp3 path:

    [credentials]
    email = you@gmail.com
    password = ***
    
    [alarm]
    query = wake
    mp3_path = /path/to/your/mp3/files/
