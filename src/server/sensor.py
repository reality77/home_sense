import json

with open('config.json') as json_data_file:
    config = json.load(json_data_file)
    DATA_DIR = config['server']['data_directory']
    config = config['clients']

DELAY = 5000

COLOR_VIOLET = [0xFF, 0x00, 0xFF]
COLOR_LIGHT_VIOLET = [0x88, 0x00, 0xFF]
COLOR_BLUE = [0x00, 0x00, 0xFF]
COLOR_LIGHT_BLUE = [0x44, 0x66, 0xFF]
COLOR_GREEN_BLUE = [0x00, 0xFF, 0xFF]
COLOR_GREEN = [0x00, 0xFF, 0x33]
COLOR_YELLOW_GREEN = [0x88, 0xFF, 0x00]
COLOR_YELLOW = [0xFF, 0xDD, 0x00]
COLOR_ORANGE = [0xFF, 0x77, 0x00]
COLOR_RED = [0xFF, 0x00, 0x00]

#****************************************************************

class Sensor:
	def __init__(self):
		global config
		self.id_client = 0
		self.client = None
		self.ledData = None

	def readInt(self, highValue, lowValue):
		val = (highValue << 8) + lowValue
		return val

	def onRun(self, timerSec):
		if (not(self.client is None) and ((self.lastApiCallTimer is None) or (timerSec - self.lastApiCallTimer > DELAY))):
                        self.lastApiCallTimer = timerSec
			sensors = self.client['sensors']

			ledcountBySensor = len(sensors) / 30
			led_index = 0
			data = [0x02]

			#read client file
			f = None
			filedata = bytearray()
			try:
				f = open(DATA_DIR + str(self.id_client), "r")
				x = f.read(1)
				while x != "":
					filedata.append(x)
					x = f.read(1)
			finally:
				if not(f is None):
					f.close()
			index = 0
			for sensor in sensors:
				type = sensor['type']
				max_value = sensor['max_value']
				print "sensor index = " + str(index)

				# read sensor data (2 bytes per sensor)
				value = self.readInt(filedata[index * 2], filedata[index * 2 + 1])
				print "value = " + str(value)

				color = COLOR_BLUE
				if type == "humidity":
					if value < 200:
						color = COLOR_ORANGE
					elif value < 400:
						color = COLOR_LIGHT_BLUE
					else:
						color = COLOR_BLUE
				elif type == "light":
					color = COLOR_YELLOW

				led_index = led_index + ledcountBySensor
				index += 1

			data.append(int(value * ledcountBySensor / max_value))
			data.extend(color)
			self.ledData = bytearray(data)
			return True
		else:
			return False

	def onSelect(self):
		global config
		self.lastApiCallTimer = None
		self.id_client = 1
		self.client = config[0] #TODO find by id_client
		return self.client['text']

	def getLedData(self):
		return self.ledData

	def onStop(self):
		return

#--------------------------
if __name__ == '__main__':

	w = Sensor()
	w.onSelect()
	w.onRun(1)
	print bytes(w.getLedData())

