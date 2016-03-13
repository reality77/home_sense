#!/usr/bin/python

import time
import datetime
from display import Display

# ===========================================================================
# Clock Example
# ===========================================================================
segment = Display(address=0x70)

print "Press CTRL+Z to exit"

# Continually update the time on a 4 char, 7-segment display
while(True):
  now = datetime.datetime.now()
  hour = now.hour
  minute = now.minute
  second = now.second
  # Set hours
  segment.writeChar(0, 'A')
  segment.writeChar(1, 'Z')
  segment.writeChar(2, 'C')
  segment.writeChar(3, 'D')
  #segment.writeDigit(0, 0xF)     # Tens
  #segment.writeDigit(1, 0xF)          # Ones
  # Set minutes
  #segment.writeDigit(3, 0xF)   # Tens
  #segment.writeDigit(4, OxF)        # Ones
  # Wait a quarter second (less than 1 second to prevent colon blinking getting in phase with odd/even seconds).
  time.sleep(1)
