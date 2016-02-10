# -*- coding: iso-8859-15 -*-
import time

import pigpio
#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''

START "sudo pigpiod" before running

'''

import vw

LED_COM_TX=21
LED_COM_BPS=2000
COLOR_RESET = bytearray([0x00]) # premier octet : mode (0 = reset)

# Exemple mode 1
#color_data0 = bytearray([0x01,          # premier octet : mode (1 = set led colors)
#             0x00, 0x00, 0x00, 0x00,   # no_led / R / G / B
#             0x01, 0xFF, 0xFF, 0x00   # no_led / R / G / B
#               ])

class LedCommunication:

   

   def __init__(self):
      return

   def setPi(self, pi):
      self.ledcom_pi = pi
      self.ledcom_tx = vw.tx(self.ledcom_pi, LED_COM_TX, LED_COM_BPS) 
     
   def sendLedColors(self, data_array):
      return self.sendToLed(data_array)

   def sendLedReset(self):
      return self.sendToLed(COLOR_RESET)

   def sendToLed(self, data_array):
     while not self.ledcom_tx.ready():
         time.sleep(0.05)
     time.sleep(0.1)

     v = self.ledcom_tx.put(data_array);
     time.sleep(0.1)
     v = self.ledcom_tx.put(data_array);
     time.sleep(0.1)
     v = self.ledcom_tx.put(data_array);
     time.sleep(0.1)
     return v

   def close(self): 
      self.ledcom_tx.cancel()

# ****************************** TEST **************************

if __name__ == "__main__":


   color_data0 = bytearray([0x01,          # premier octet : mode (1 = set led colors)
             0x00, 0x00, 0xFF, 0x00,   # no_led / R / G / B
             0x01, 0xFF, 0xFF, 0x00,   # no_led / R / G / B
             0x02, 0xFF, 0x00, 0xFF  # no_led / R / G / B

                        ])

   color_data_all_part1 = bytearray([0x01,          # premier octet : mode (1 = set led colors)
             0x00, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x01, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x02, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x03, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x04, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
])
   color_data_all_part2 = bytearray([0x01,          # premier octet : mode (1 = set led colors)
             0x05, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x06, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x07, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x08, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x09, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
])
   color_data_all_part3 = bytearray([0x01,          # premier octet : mode (1 = set led colors)
             0x0A, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x0B, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x0C, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x0D, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x0E, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
])
   color_data_all_part4 = bytearray([0x01,          # premier octet : mode (1 = set led colors)
             0x0F, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x10, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x11, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x12, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x13, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
            ])

   color_data_all_part5 = bytearray([0x01,          # premier octet : mode (1 = set led colors)
             0x14, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x15, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x16, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x17, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x18, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
])
   color_data_all_part6 = bytearray([0x01,          # premier octet : mode (1 = set led colors)
             0x19, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x1A, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x1B, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x1C, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x1D, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
            ])

   color_data_12 = bytearray([0x01,          # premier octet : mode (1 = set led colors)
             0x00, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x01, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x02, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x03, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x04, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             0x05, 0xFF, 0xFF, 0xFF#,   # no_led / R / G / B
             #0x06, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             #0x07, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             #0x08, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             #0x09, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             #0x0A, 0xFF, 0xFF, 0xFF,   # no_led / R / G / B
             #0x0B, 0xFF, 0xFF, 0xFF   # no_led / R / G / B
                            ])

   color_data_withcount = bytearray([0x02,          # premier octet : mode (2 = set led colors count)
             0x0A, 0x00, 0x00, 0xFF,   # nbre_led / R / G / B
             0x0A, 0xFF, 0xFF, 0xFF,   # nbre_led / R / G / B
             0x0A, 0xFF, 0x00, 0x00,   # nbre_led / R / G / B
            ])
   


   _ledcom = LedCommunication()

   for i in range(0, 30):
      print "sending reset"
      result = _ledcom.sendLedReset()
      print "-> " + str(result)
      time.sleep(5)
      print "sending 1 LED color"
      result = _ledcom.sendLedColors(color_data0)
      print "-> " + str(result)
      time.sleep(5)
      print "sending 12 LED"
      result = _ledcom.sendLedColors(color_data_12)
      print "-> " + str(result)
      time.sleep(5)
      print "sending all LED"
      result = _ledcom.sendLedColors(color_data_withcount)
      #result = _ledcom.sendLedColors(color_data_all_part1)
      #print "-> " + str(result)
      #time.sleep(1)
      #result = _ledcom.sendLedColors(color_data_all_part2)
      #print "-> " + str(result)
      #time.sleep(1)
      #result = _ledcom.sendLedColors(color_data_all_part3)
      #print "-> " + str(result)
      #time.sleep(1)
      #result = _ledcom.sendLedColors(color_data_all_part4)
      #print "-> " + str(result)
      #time.sleep(1)
      #result = _ledcom.sendLedColors(color_data_all_part5)
      #print "-> " + str(result)
      #time.sleep(1)
      #result = _ledcom.sendLedColors(color_data_all_part6)
      print "-> " + str(result)
      time.sleep(3)

   print "closing"
   _ledcom.close()

   print "End"


   
