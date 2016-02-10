# Home Sense
Home sense server

The objective of this project is to create a smart LED strip you can place everywhere in the house.

With the home_sense project you can :
- know the best timing to take your bus/tramway/subway
- display the next 12 hours temperatures
- and all other meanings you can bring to a LED strip

The server part (doing the 'smart business') sends the data to the LED Strip part

## Server part

### Hardware

The server part is composed of :
- A Rasperry Pi 2 running on Raspbian and connected to the Internet
- 2 buttons :
	- A MODE button : with this, you can switch the mode of the LED strip :
		- display bus data
		- display weather data
		- turn off the Raspberry Pi
		- and other stuff you can write like 
	- A SELECT button : with this, you can select the option of the current mode:
		- With bus data,  switch to another preloaded target address
		- With weather data, switch from temperatures display to conditions display
		- etc...
- A 4 alphanumeric digits LED display will show you the modes and selection you have made
- A 433 Mhz emitter, to send the data to the LED Strip 
(- A 433 Mhz receiver to receive data from other components - NOT USED YET)

You can download the [Server Fritzing file](fritzing/server.fzz).

### Software

The src folder contains the python scripts to run the server part.
The [main.py](src/main.py) file contains the main functions of the server.
Each server _mode_ is a python class called by the main module:
- [busgo.py](src/busgo.py) contains the bus mode software
- [weather.py](src/weather.py) contains the weather mode software

The communication with the led strip is held by the [led_communication.py file](src/led_communication.py) and uses the virtualwire python implementation

## LED Strip display part

### Hardware

The LED Strip part is composed of :
- An Arduino Uno to drive the LED Strip
- An AdaFruit Digital LED Strip (30 LED - 1 meter)
- A 433 Mhz receiver to receive data from the server (Raspberry Pi 2)

You can download the [LED Strip part Fritzing file](fritzing/ardled.fzz).

### Software
(The arduino software is not yet in that repository - COMING SOON)

# Configuration

A _config.json_ file should be present in the src folder. This file is not uploaded in the repository for security purposes.
If you have not one, copy the [demo file](src/demo_config.json) to _config.json_ and edit it

If you wish to use the weather temperature data, fill the weather parameters : 
- city
- openweather_apikey


If you wish to use the busgo data, fill the parameters : 
- gmaps_key (you have to get a google maps API Key with Directions API enabled)
- create a direction data (gmaps_directions) :
	- id (unique)
	- a small text to quickly identify the target address (4 letters max - for alphanumeric led display)
	- the source address (source_address)
	- the target address (target_address)

# Thank to ...

... other projects contributors :
- [VirtualWire implementation for Raspberry Pi](../../joan2937/pigpio)
- [google maps services for python](../../googlemaps/google-maps-services-python)