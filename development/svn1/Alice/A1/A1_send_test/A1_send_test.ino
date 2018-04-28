/*
  Program to test sending a blinking infrared signal (with 38 kHz
  carrier frequency) to the receiving party. 
  The library only supports sending IR signal with pin 3.
  
  Author: Qcumber2018
*/

#include <IRremote.h>
IRsend irsend;

// Parameter declaration
int blink_period = 500;  // in ms

// Other parameters declarations
// -- only modify this if you know what you are doing --
unsigned int carrier_freq = 38; // in kHz


void setup(){
  // Enable the IR pin and set the carrier frequency
  irsend.enableIROut(carrier_freq);
}


void loop(){
  // bright
  TIMER_ENABLE_PWM;
  delay(blink_period);
  // dark
  TIMER_DISABLE_PWM;
  delay(blink_period);
}

