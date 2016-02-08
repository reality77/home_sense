import urllib2, urllib, json

with open('config.json') as json_data_file:
    config = json.load(json_data_file)['weather']

API_KEY = config['openweather_apikey']
API_URL = config['openweather_apiurl']
API_COUNT_DATA = config['api_3hblocks_count'] # 4 data blocks of 3hours per block = 12 hours of data
API_CALL_DELAY = 30 * 60 #30 minutes

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


W_THUNDER__MIN = 200
W_THUNDER_W_LIGHT_RAIN = 200 	#thunderstorm with light rain 	11d 
W_THUNDER_W_RAIN = 201 			# 	thunderstorm with rain 	11d 
W_THUNDER_W_HEAVY_RAIN = 202 	#thunderstorm with heavy rain 	11d 
W_THUNDER_LIGHT = 210 			# light thunderstorm  11d 
W_THUNDER = 211 				# 	thunderstorm 	11d 
W_THUNDER_HEAVY = 212  			#heavy thunderstorm 	11d 
W_THUNDER_RAGGED = 221 			#ragged thunderstorm 	11d 
W_THUNDER_W_LIGHT_DRIZZLE = 230 #thunderstorm with light drizzle 	11d 
W_THUNDER_W_DRIZZLE = 231 		#thunderstorm with drizzle 	11d 
W_THUNDER_W_HEAVY_DRIZZLE = 232 #thunderstorm with heavy drizzle 	11d
W_THUNDER__MAX = 299
	
W_DRIZZLE__MIN = 300
W_DRIZZLE_LIGHT = 300 			#light intensity drizzle 	09d 
W_DRIZZLE = 301					#drizzle = bruine, crachin 09d
W_DRIZZLE_HEAVY = 302 			#heavy intensity drizzle 	09d 
W_DRIZZLE_RAIN_LIGHT = 310		#light intensity drizzle rain 	09d 
W_DRIZZLE_RAIN = 311 				#drizzle rain 	09d 
W_DRIZZLE_RAIN_HEAVY = 312 			#heavy intensity drizzle rain 	09d
W_DRIZZLE_SHOWER_RAIN = 313 		#shower rain and drizzle 	09d
W_DRIZZLE_HEAVY_SHOWER_RAIN = 314 	#heavy shower rain and drizzle 	09d
W_DRIZZLE_SHOWER = 321 		#shower drizzle 	09d 
W_DRIZZLE__MAX = 399
	
W_RAIN__MIN = 500
W_RAIN_LIGHT = 500 			#light rain 	10d
W_RAIN_MODERATE = 501 		#moderate rain 	10d
W_RAIN_HEAVY = 502 			#heavy intensity rain 	10d
W_RAIN_VERY_HEAVY = 503 	#very heavy rain 	10d
W_RAIN_EXTREME = 504 		#extreme rain 	10d
W_RAIN_FREEZING = 511 		#freezing rain 	13d
W_RAIN_LIGHT_SHOWER = 520 	#light intensity shower rain 	09d
W_RAIN_SHOWER = 521 		#shower rain 	09d
W_RAIN_HEAVY_SHOWER = 522 	#heavy intensity shower rain 	09d
W_RAIN_RAGGED_SHOWER = 531 	#ragged shower rain 	09d 
W_RAIN__MAX = 599
	
W_SNOW__MIN = 600
W_SNOW_LIGHT = 600 			#light snow 	[[file:13d.png]]
W_SNOW = 601 				#snow 	[[file:13d.png]]
W_SNOW_HEAVY = 602 			#heavy snow 	[[file:13d.png]]
W_SNOW_SLEET = 611 			#sleet = gresil, neige fondue
W_SNOW_SHOWER_SLEET = 612 	#shower sleet 	[[file:13d.png]]
W_SNOW_LIGHT_RAIN = 615 	#light rain and snow 	[[file:13d.png]]
W_SNOW_RAIN = 616 			#rain and snow 	[[file:13d.png]]
W_SNOW_LIGHT_SHOWER = 620 	#light shower snow 	[[file:13d.png]]
W_SNOW_SHOWER =621 			#shower snow 	[[file:13d.png]]
W_SNOW_HEAVY_SHOWER = 622 	#heavy shower snow 	[[file:13d.png]] 
W_SNOW__MAX = 699
	
W_OTHER__MIN = 700
W_OTHER_MIST = 701 				#mist = brume 	[[file:50d.png]]
W_OTHER_SMOKE = 711 			#smoke 	[[file:50d.png]]
W_OTHER_HAZE = 721 				#haze 	[[file:50d.png]]
W_OTHER_SAND_DUST = 731 		#sand, dust whirls 	[[file:50d.png]]
W_OTHER_FOG = 741 				#fog 	[[file:50d.png]]
W_OTHER_SAND = 751 				#sand 	[[file:50d.png]]
W_OTHER_DUST = 761 				#dust 	[[file:50d.png]]
W_OTHER_VOLCANIC_ASH = 762 		#volcanic ash 	[[file:50d.png]]
W_OTHER_SQUALLS = 771 			#squalls = bourasques, rafales 	[[file:50d.png]]
W_OTHER_TORNADO = 781 			#tornado 	[[file:50d.png]] 
W_OTHER__MAX = 799
	
W_CLEAR = 800 					#clear sky 	[[file:01d.png]] [[file:01n.png]] 

W_CLOUDS__MIN = 801
W_CLOUDS_FEW = 801 			#few clouds 	[[file:02d.png]] [[file:02n.png]]
W_CLOUDS_SCATTERED = 802 	#scattered clouds 	[[file:03d.png]] [[file:03d.png]]
W_CLOUDS_BROKEN = 803 		#broken clouds 	[[file:04d.png]] [[file:03d.png]]
W_CLOUDS_OVERCAST = 804 	#overcast clouds 	[[file:04d.png]] [[file:04d.png]] 
W_CLOUDS__MAX = 899
	
W_WIND__MIN = 900
W_WIND_TORNADO = 900 		#tornado
W_WIND_TROPICALSTORM = 901 	#tropical storm
W_WIND_HURRICANE = 902 		#hurricane
W_WIND_COLD = 903 			#cold
W_WIND_HOT = 904 			#hot
W_WIND_WINDY = 905 			#windy
W_WIND_HAIL = 906 			#hail 
W_WIND__MAX = 900

W_BEAUFORT__MIN = 951
W_BEAUFORT_1 = 951 			#calm (= force 1 de beaufort)
W_BEAUFORT_2 = 952 			#light breeze
W_BEAUFORT_3 = 953 			#gentle breeze
W_BEAUFORT_4 = 954 			#moderate breeze
W_BEAUFORT_5 = 955 			#fresh breeze
W_BEAUFORT_6 = 956 			#strong breeze
W_BEAUFORT_7 = 957 			#high wind, near gale
W_BEAUFORT_8 = 958 			#gale
W_BEAUFORT_9 = 959 			#severe gale
W_BEAUFORT_10 = 960 		#storm
W_BEAUFORT_11 = 961 		#violent storm
W_BEAUFORT_12 = 962 		#hurricane 
W_BEAUFORT__MAX = 962

#****************************************************************

class WeatherCondition:
	def __init__(self):
		self.temp = -1
		self.humidity = -1
		self.pressure = -1
		self.city = ""
		self.condition = -1
		self.cloud_percent = -1
		self.rain3h = -1
		self.snow3h = -1
		self.wind_speed = -1
		self.wind_direction = -1


#****************************************************************

class Weather:

	def __init__(self):
		global config
		self.city = config['city']
		self.lastApiCallTimer = None
		self.ledData = None

	def callWeatherApi(self):
		global API_URL, API_KEY, API_COUNT_DATA
		url = API_URL.format(self.city, API_KEY, API_COUNT_DATA)
		print url
		result = urllib2.urlopen(url).read()
		data = json.loads(result)
		return data

	def getWeatherConditions(self, weatherData, index):
		result = WeatherCondition()
		w = weatherData['list'][index]
		result.temp = w['main']['temp']
		result.humidity = w['main']['humidity']
		result.pressure = w['main']['pressure']
		
		result.condition = w['weather'][0]['id']
		result.cloud_percent = w['clouds']['all']
		result.rain3h = w['rain'].get('3h', 0)
		snow = w.get('snow', 0)
		if snow != 0:
			result.snow3h = w['snow'].get('3h', 0)
		else:
			result.snow3h = 0
		result.wind_speed = w['wind'].get('speed', 0)
		result.wind_direction = w['wind'].get('deg', 0)
		return result

	def onRun(self, timerSec):
		if (self.lastApiCallTimer is None) or (timerSec - self.lastApiCallTimer > API_CALL_DELAY):
                        self.lastApiCallTimer = timerSec
			rawdata = self.callWeatherApi()
			data = [0x02]
			ledByHour = 24 / API_COUNT_DATA / 3
			for i in range(0, API_COUNT_DATA):
				data0 = self.getWeatherConditions(rawdata, i)
				print data0.temp
				data.append(ledByHour * 3)
				if data0.temp <= -10:
					data.extend(COLOR_VIOLET)
				elif data0.temp < -5:
					data.extend(COLOR_LIGHT_VIOLET)
				elif data0.temp < 0:
					data.extend(COLOR_BLUE)
				elif data0.temp < 5:
					data.extend(COLOR_LIGHT_BLUE)
				elif data0.temp < 10:
					data.extend(COLOR_GREEN_BLUE)
				elif data0.temp < 15:
					data.extend(COLOR_GREEN)
				elif data0.temp < 20:
					data.extend(COLOR_YELLOW_GREEN)
				elif data0.temp < 25:
					data.extend(COLOR_YELLOW)
				elif data0.temp < 30:
					data.extend(COLOR_ORANGE)
				elif data0.temp < 35:
					data.extend(COLOR_RED)
				elif data0.temp >= 35:
					data.extend(COLOR_VIOLET)
			self.ledData = bytearray(data)
			return True
		else:
			return False

	def onSelect(self):
		self.lastApiCallTimer = None
		return "W"

	def getLedData(self):
		return self.ledData

	def onStop(self):
		return

#--------------------------
if __name__ == '__main__':

	w = Weather()
	w.onSelect()
	w.onRun(1)
	print w.getLedData()

