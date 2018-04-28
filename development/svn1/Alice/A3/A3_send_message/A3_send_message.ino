/*
  Program to send a string of characters via the NEC-string
  protocol.
  The library only supports sending IR signal with pin 3.
  
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
  while(!Serial.available());
  char strbuf[4] = ""; // send 4 characters each time
  Serial.readBytes(strbuf, 4); // Read 4 characters each time
  unsigned long value = (unsigned long) strbuf[0] << 24 
                      | (unsigned long) strbuf[1] << 16
                      | (unsigned long) strbuf[2] << 8
                      | (unsigned long) strbuf[3];
  Serial.print(value, HEX);  // Debug                   
  irsend.sendNEC(value, 32);   // Send the characters
}

