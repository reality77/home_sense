//https://skyduino.wordpress.com/2011/12/29/tutoriel-arduino-et-emetteurrecepteur-433mhz-virtualwire/
// Émission d'un message a 433 MHz par l'Arduino

// basé sur:
// transmitter.pde
//
// Simple example of how to use VirtualWire to transmit messages
// Implements a simplex (one-way) transmitter with an TX-C1 module
//
// See VirtualWire.h for detailed API docs
// Author: Mike McCauley (mikem@airspayce.com)
// Copyright (C) 2008 Mike McCauley
// $Id: transmitter.pde,v 1.3 2009/03/30 00:07:24 mikem Exp $

#include <VirtualWire.h>

int counter = 0;

void setup()
{
    Serial.begin(9600);    // Debugging only
    Serial.println("Demarrage");
    pinMode(13, OUTPUT);
    pinMode(A1, INPUT);

    // Initialise the IO and ISR
    vw_set_tx_pin(7);
    vw_set_ptt_inverted(true); // Required for DR3100
    vw_setup(2000);  // Bits per sec
    digitalWrite(13, LOW);
}

void loop()
{
    counter++;

    int humidity = analogRead(A0);
    int light = analogRead(A1);
    
    Serial.print("Moisture Sensor Value:");
    Serial.println(humidity);  
    Serial.print("Light Sensor Value:");
    Serial.println(light);  
    
    int LEN_DATA = 6;
    byte data[LEN_DATA];
    data[0] = 0xFE; // "sensor" mode for server 
    data[1] = 0x01; // sensor ID
    data[2] = light >> 8; // light sensor value (high)
    data[3] = light ^ (data[2] << 8); // light sensor value (low)
    data[4] = humidity >> 8; // moisture sensor value (high)
    data[5] = humidity ^ (data[4] << 8); // moisture sensor value (low)
    
    Serial.print("Prepare to send\r\n");

    digitalWrite(13, HIGH); // Flash a light to show transmitting
    vw_send(data, LEN_DATA);
    vw_wait_tx(); // Wait until the whole message is gone
    delay(500);
    vw_send(data, LEN_DATA);
    vw_wait_tx(); // Wait until the whole message is gone
    delay(500);
    vw_send(data, LEN_DATA);
    vw_wait_tx(); // Wait until the whole message is gone
    digitalWrite(13, LOW);

    Serial.print("Data sent\r\n");
    //delay(60000000);
    delay(30000);
}
