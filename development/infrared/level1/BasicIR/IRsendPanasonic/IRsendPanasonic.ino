/*
  A simple program to send IR signal to a Panasonic Projector device
  Please modify the command bytes below to send the command that you desire.
  
  Author: Qcumber 2018
*/

#include <IRremote.h>

// The array contains information about the timing for ON and OFF sequences
unsigned int irSignal[] = {3350, 1800, // Header
// Address byte 1
350,  550,  350, 1400,  350,  550,  350,  550,  // 4
350,  550,  350,  550,  350,  550,  350,  550,  // 0
// Address byte 2
350,  550,  350,  550,  350,  550,  350,  550,  // 0
350,  550,  350, 1400,  350,  550,  350,  550,  // 4
// Address byte 3
350,  550,  350,  550,  350,  550,  350,  550,  // 0
350,  550,  350,  550,  350,  550,  350, 1400,  // 1
// Address byte 5
350,  550,  350,  550,  350,  550,  350, 1400,  // 1
350,  550,  350,  550,  350, 1400,  350,  550,  // 2
// Address byte 6
350,  550,  350,  550,  350,  550,  350,  550,  // 0 
350,  550,  350,  550,  350,  550,  350,  550,  // 0
// Command byte 1
350, 1400,  350,  550,  350, 1400,  350, 1400,  // ?
350, 1400,  350, 1400,  350,  550,  350,  550,  // ?
// Command byte 2
350, 1400,  350,  550,  350, 1400,  350,  550,  // ?
350, 1400,  350, 1400,  350, 1400,  350, 1400,  // ? 
// Stop pulse
350 };

IRsend irsend;

void setup()
{
// Set pin 13 as a reference (when a stream of signal is sent)
pinMode(13, OUTPUT);
  
}

void loop() {
  int khz = 38; // 38kHz carrier frequency 
 
  digitalWrite(13, HIGH);
  irsend.sendRaw(irSignal, sizeof(irSignal) / sizeof(irSignal[0]), khz); //Note the approach used to automatically calculate the size of the array.
  digitalWrite(13, LOW);

  delay(100); // Repeat every 100 ms
}
