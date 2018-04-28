/*
  Program to receive a blinking infrared signal (with 38 kHz
  carrier frequency) from the sending party, and sends a "ON"
  word and counter every time it detects the light via serial 
  monitor.
  
  Please use Ctrl+Shift+M to start the serial monitor 
  
  Author: Qcumber2018
*/

#include <IRremote.h>
IRsend irsend;

// Parameter declaration
int recv_pin = 11;

// Other parameters declarations
// -- only modify this if you know what you are doing --
int reset_time = 150; // in ms
int counter = 0; 


void setup(){
  // Open up the serial communication
  Serial.begin(9600);
  // Set the recv_pin to INPUT
  pinMode(recv_pin, INPUT);
}


void loop(){
  // Reading the receiving pin output
  int readout = digitalRead(recv_pin);
  if (!readout){    
    counter += 1; // Increment the counter
    // Detected a IR light
    Serial.print("ON ");
    Serial.println(counter);
    delay(reset_time);
  } 
}

