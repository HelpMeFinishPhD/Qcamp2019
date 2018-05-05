/*
  First attempt to recapitulate all the features in infrared comm (Mission 1).
  Implemented features:
  1. Send Blinking feature
  2. Recv Blinking feature
  3. Sending a short message (4 bytes)
  4. Recving a short message (4 bytes)
 Author: Adrian Utama (2018) 
*/

#include <IRremote.h>

// Parameters
const int serial_timeout = 100; // 100 ms 
const int send_pin = 3;  // The library sets it to 3 (fixed).
const int recv_pin = 11; // Pin 11

// More useless parameters
int blink_time = 200;     // 200 ms
int blink_num = 20;       // 20 blinks
int blink_obtime = 10000; // 10 seconds
int blink_rstime = 300;   // 300 ms timeout 
    
// initialize the IR library
IRsend irsend;         
IRrecv irrecv(recv_pin);
decode_results results;

void setup() {
  // initialize the serial port:
  Serial.begin(9600);
  Serial.setTimeout(serial_timeout);
}

void loop() {
  // Select the best response
  while (!Serial.available()); // Listen to serial input
  char serbuf[8] = ""; // Reinitialise buffer (8 bytes)
  Serial.readBytesUntil(' ', serbuf, 8); // Until whitespace
  // Obtain which input command (enumerated)
  int enumc = -1; // default choice
  int maxChoice = 5;
  char sercmd[maxChoice][8] = {"HELP", "SBLINK", "RBLINK", "SEND", "RECV"};
  for (int c=0; c<maxChoice; c++){
    if (strcasecmp(sercmd[c],serbuf) == 0){ 
      enumc = c;// Obtain match
    }
  }
  
  // Declaring some other parameters
  unsigned long timeNow;
  unsigned long timeEnd;
  int readout;
  
  // Switching between different cases
  switch(enumc){
    case 0: //HELP
      Serial.print("Stepper Motor Implementation Level 1\n");
      Serial.print("HELP       Print help statement\n");
      Serial.print("SBLINK     Send blinking feature\n");
      Serial.print("RBLINK     Recv blinking feature\n");
      Serial.print("SEND X     Send a short message X (4 bytes)\n");
      Serial.print("RECV       Receive a short message\n");
      break; 
    case 1: //SBLINK
      // Serial.print("Perform some blinking features \n");
      for (int i=0; i<blink_num; i++){
        digitalWrite(send_pin, HIGH);
        delay(blink_time);
        digitalWrite(send_pin, LOW);
        delay(blink_time);        
      }
      Serial.println("Task done.");
      break;
    case 2: //RBLINK
      // Serial.print("Trying to recv blinking features \n");
      // listen for blink during blink_obtime
      timeNow = millis(); // get time now
      timeEnd = timeNow + blink_obtime;
      while (timeNow < timeEnd){
        readout = digitalRead(recv_pin);
        if (!readout){    
          // Detected an IR light blinking
          Serial.print("BLINK!");
          delay(blink_rstime);
        } 
      }
      Serial.println("Task done.");
      break;
    case 3: //SEND X
      Serial.print("Trying to send a word \n");
    case 4: //POLOFF
      Serial.print("Trying to recv a word \n");
    default:
      Serial.print("Unknown command\n");
      break;
  }
}

