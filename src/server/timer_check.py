#!/usr/bin/python

# Thanks to contributors of https://github.com/googlemaps/google-maps-services-python

from datetime import datetime
from datetime import timedelta
import time
import json

TIMER_EACH_DAY = 0
TIMER_EACH_WEEKDAY = 1
TIMER_EACH_WEEKENDDAY = 2

with open('config.json') as json_data_file:
    config = json.load(json_data_file)['timers']

class TimerCheck:

    def __init__(self):
	global config
        self.timers = config
        self.current_timer = None
 
    # **************** Maps API
    def check(self):
        global config
	weekday = datetime.today().weekday()
	currentTime = datetime.now().replace(year=1900, month=1, day=1).timetuple()
	processDay = 0
	self.current_timer = None
	for tmr in self.timers:
	    # find out if the timer object can run on the current day
	    if tmr['type'] == TIMER_EACH_DAY:
		processDay = 1
	    elif tmr['type'] == TIMER_EACH_WEEKDAY:
		if weekday >= 0 and weekday <= 4:
		    processDay = 1
   	    elif tmr['type'] == TIMER_EACH_WEEKENDDAY:
		if weekday == 5 or weekday == 6:
		    processDay = 1

	    # test if the timer object can run in the current time
	    if processDay:
		start = time.strptime(tmr['start-time'], "%H:%M:%S")
		end = time.strptime(tmr['end-time'], "%H:%M:%S")
		if currentTime >= start and currentTime <= end:
		    self.current_timer = tmr
		    break

	return self.current_timer

# ****************************** TEST **************************

if __name__ == "__main__":
    t = TimerCheck()
    print t.check()
