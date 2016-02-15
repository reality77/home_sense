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

int compteur = 0;

const char *msg = "GASPARD-";
char nombre[VW_MAX_MESSAGE_LEN];
char message[VW_MAX_MESSAGE_LEN]; 

void setup()
{
    //Serial.begin(9600);    // Debugging only

    pinMode(13, OUTPUT);

    // Initialise the IO and ISR
    vw_set_ptt_inverted(true); // Required for DR3100
    vw_setup(2000);  // Bits per sec
    digitalWrite(13, LOW);
}

void loop()
{
    compteur++;

    int humidite = analogRead(A0);

    //Serial.print("Moisture Sensor Value:");
    //Serial.println(humidite);  
    
    // Conversion du int en tableau de chars
    itoa(humidite,nombre,10); // 10 car décimal
    strcpy (message, msg);
    strcat(message,nombre);

    //Serial.print("Préparation envoi\r\n");

    digitalWrite(13, HIGH); // Flash a light to show transmitting
    vw_send((uint8_t *)message, strlen(message));
    vw_wait_tx(); // Wait until the whole message is gone
    digitalWrite(13, LOW);

    //Serial.print("Envoi OK\r\n");
    delay(60000);
}
