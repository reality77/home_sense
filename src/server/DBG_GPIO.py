IN = 0
OUT = 1
BOARD = 0
BCM = 1
PUD_DOWN = 0
PUD_UP = 1
RISING = 1
FALLING = 0

def setmode(val):
	print "GPIO - Set Mode : " + str(val)
	return

def setup(pin, direction, pull_up_down):
	print "GPIO setup pin \#" + str(pin) + " - mode : " + str(direction)
	return

def add_event_detect(pin, event, callback, bouncetime):
	print "GPIO event NO SET for pin \#" + str(pin)

def cleanup():
	print "GPIO cleanup"
