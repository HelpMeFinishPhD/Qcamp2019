/*
  Program to send a binary signal via NEC protocol to 
  the receiving party.
  The library only supports sending IR signal with pin 3.
  
  Please use Ctrl+Shift+M to start the serial monitor 
  
  Author: Qcumber2018
*/

#include <IRremote.h>

// Parameter declaration
// --- nothing to declare ---

// Other parameters declarations
// -- only modify this if you know what you are doing --
int serial_timeout = 100; // 100 ms 

IRsend irsend;

void setup(){
  // Open up the serial communication
  Serial.begin(9600);
  Serial.setTimeout(serial_timeout);
}


void loop(){
  while(!Serial.available());  // Listen to serial input
  char strbuf[8] = "";         // Initialise the buffer char array
  Serial.readBytes(strbuf, 8); // Read one character at a time
  // Magic command to convert binary string to int
  unsigned int strval = strtol(strbuf, (char**) NULL, 2); 
  irsend.sendNEC(strval, 32);  // Send the character via NEC
}

