#include <VirtualWire.h> // inclusion de la librairie VirtualWire
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6
#define PIN_LED 2
#define PIN_INTERNAL_LED 13
#define LED_COUNT 30

Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);

void setup()
{
    Serial.begin(9600); // Initialisation du port série pour avoir un retour sur le serial monitor

    char data[255];
    sprintf(data, "Demarrage. Max Length = %d", VW_MAX_MESSAGE_LEN);
    Serial.println(data);

    vw_setup(2000); // initialisation de la librairie VirtualWire à 2000 bauds (note: je n'utilise pas la broche PTT)
    vw_set_rx_pin(11);
    vw_rx_start();  // Activation de la partie réception de la librairie VirtualWire

    pinMode(PIN_LED, OUTPUT);
    pinMode(PIN_INTERNAL_LED, OUTPUT);

    strip.begin();
    strip.setBrightness(8);
    strip.show(); // Initialize all pixels to 'off'
}
 
void loop()
{
    uint8_t buf[VW_MAX_MESSAGE_LEN]; // Tableau qui va contenir le message reçu (de taille maximum VW_MAX_MESSAGE_LEN)
    uint8_t buflen = VW_MAX_MESSAGE_LEN; // Taille maximum de notre tableau

    bool pixelSet = false;

    int current_mode = -1;
    uint8_t current_data[VW_MAX_MESSAGE_LEN];
    uint8_t current_data_len = 0;
    
    if (vw_wait_rx_max(1000)) // Si un message est reçu dans les 200ms qui viennent
    {
        digitalWrite(PIN_LED, HIGH);

        if (vw_get_message(buf, &buflen)) // On copie le message, qu'il soit corrompu ou non
        {
            digitalWrite(PIN_INTERNAL_LED, HIGH);
            int mode = (int)buf[0];
      
            char data[255];
            sprintf(data, "RX : mode = %d", mode);
            Serial.println(data);
            
            switch(mode)
            {
              case 0:
              {
                Serial.println("Mode 0 detected");
                current_mode = mode;
                current_data_len = buflen;
                memcpy(&current_data, &buf, current_data_len);
              }
              break;
              case 1: // chaque donnée : no_led / R / G / B
              {
                Serial.println("Mode 1 detected");
                int ok = (buflen - 1) % 4; // 4 octets par LED
                if(ok == 0 && buflen > 0)
                {
                  current_mode = mode;
                  current_data_len = buflen;
                  memcpy(&current_data, &buf, current_data_len);
                }
                else
                  Serial.println("Donnees non valide pour le mode");
              }
              break;
              case 2: // chaque donnée : nbre_led / R / G / B
              {
                Serial.println("Mode 2 detected");
                int ok = (buflen - 1) % 4; // 4 octets par groupe de données
                if(ok == 0 && buflen > 0)
                {
                  current_mode = mode;
                  current_data_len = buflen;
                  memcpy(&current_data, &buf, current_data_len);
                }
                else
                  Serial.println("Donnees non valide pour le mode");
              }
              break;
            }

            digitalWrite(PIN_INTERNAL_LED, LOW);
        }
        else
          Serial.println("***** BAD DATA RECEIVED");

        digitalWrite(PIN_LED, LOW);
    }

    // --- execute command if any
    switch(current_mode)
    {
      case 0:
      {
        Serial.println("Executing mode 0");
        strip.clear();
        strip.show();
        Serial.println("Mode 0 done");
      }
      break;
      case 1: 
      {
        Serial.println("Executing mode 1");
        modeSetLedColors(current_data, current_data_len);
        Serial.println("Mode 1 done");
      }
      break;
      case 2: 
      {
        Serial.println("Executing mode 2");
        modeSetLedColorsCount(current_data, current_data_len);
        Serial.println("Mode 2 done");
      }
      break;
      case 3:
      {
        Serial.println("Executing mode 3");
        int brightness = (int)buf[1];
        strip.setBrightness(brightness);
        strip.show();
        Serial.println("Mode 3 done");
      }
     }
    
}

void modeSetLedColors(uint8_t* buf, uint8_t buflen)
{
  bool pixelSet = false;
  
  for (byte i = 1; i < buflen; i+=4) // on commence à 1 car le premier a été déjà lu (le mode)
  {
      char data[255];
      sprintf(data, "LED = %d : R=0x%x G=0x%x B=0x%x\n", buf[i], buf[i+1], buf[i+2], buf[i+3]);
      Serial.println(data);             
      
      int ledno = buf[i];
      if(ledno >= 0 && ledno < LED_COUNT)
      {
        strip.setPixelColor(ledno, strip.Color(buf[i+1], buf[i+2], buf[i+3]));
        pixelSet = true;
      }
      else
        Serial.println("Max LED atteint");
  }

  if(pixelSet)
    strip.show();
}


void modeSetLedColorsCount(uint8_t* buf, uint8_t buflen)
{
  strip.clear();

  int ledno = 0;
  int lastledno = 0;
  for (byte i = 1; i < buflen; i+=4) // on commence à 1 car le premier a été déjà lu (le mode)
  {
      char data[255];
      sprintf(data, "Nombre = %d : R=0x%x G=0x%x B=0x%x\n", buf[i], buf[i+1], buf[i+2], buf[i+3]);
      Serial.println(data);             

      int ledcount = buf[i];

      if(ledcount >= 0 && ledno < LED_COUNT)
      {
        for(; ledno - lastledno < ledcount; ledno++)
        {
          if(ledno < LED_COUNT)
          {
            strip.setPixelColor(ledno, strip.Color(buf[i+1], buf[i+2], buf[i+3]));
            sprintf(data, "LED %d set\n", ledno);
            Serial.println(data);
          }
          else
          {
            Serial.println("Max LED atteint");
            break;
          }
        }
      }
      else
        Serial.println("Max LED atteint");

     lastledno = ledno;
  }

  strip.show();
}

