#!/usr/bin/python

# Thanks to contributors of https://github.com/googlemaps/google-maps-services-python

from datetime import datetime
from datetime import timedelta
import time
import json

TIMER_EACH_DAY
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
    def checkTimer(self):
        global config
	for tmr in self.timers:
		if tmr.type == TIMER_EACH_WEEKDAY:
			#TODO: test current day of the week
		elif tmr.type == TIMER_EACH_WEEKENDDAY:
			#TODO: test current day of the week
		# TODO : Parse start and end time & Test current timer
        return self.current_timer

# ****************************** TEST **************************

if __name__ == "__main__":
	return
    
