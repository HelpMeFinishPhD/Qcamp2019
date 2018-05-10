/*
  Program to receive the binary signal via NEC protocol from
  the sending party.
  
  Please use Ctrl+Shift+M to start the serial monitor 
  
  Author: Qcumber2018
*/

#include <IRremote.h>

// Parameter declaration
// --- nothing to declare ---

// Other parameters declarations
// -- only modify this if you know what you are doing --
int recv_pin = 11;
int irrecv_timeout = 100; // 100 ms 

IRrecv irrecv(recv_pin);
decode_results results;

void setup(){
  // Open up the serial communication
  Serial.begin(9600);
  // Set the recv_pin to INPUT
  irrecv.enableIRIn();
}


void loop(){
  if (irrecv.decode(&results)) {
    Serial.print(results.value, BIN); // Print binary characters
    Serial.print(" "); // Add a white space between char
    irrecv.resume();   // Receive the next value
  }
  delay(irrecv_timeout);
}

