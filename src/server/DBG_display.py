#!/usr/bin/python

import time
import datetime

class Display:
  disp = None

  def __init__(self, address):
    print "DISPLAY : set address 0x{0:x}".format(address)

  def writeChar(self, charNumber, value):
    print "DISPLAY : set char {0} value : {1}".format(charNumber, value)
