/*
  First attempt to write the program for the stepper motor.
  Implemented features:
  1. Able to move + serial communication
  2. Perform full revolution
  3. Move to a specified angle (store this to EEPROM)
  4. Re-initialise angle (need to be performed a the end of cycle)
 Author: Adrian Utama (2018) 
*/

#include <EEPROM.h>
#include "EEPROMAnything.h"
#include <Stepper.h>

// Parameters
const int stepDirection = 1; // Clockwise
const int stepDelay = 2; // 2 ms
const int stepSpeed = 1000; // 1000 rpm: any number high enough would do
const int stepsPerRevolution = 2048; 

const int serialTimeout = 100; // 100 ms

const int EEloc_angleCurrent = 0; // Takes 2 bytes
const int EEloc_angleTarget = 2;  // Takes 2 bytes
    
// initialize the stepper library on pins 8 through 11:
// need to swap pins 10 and 9 (due to wiring reason)
Stepper myStepper(stepsPerRevolution,8,10,9,11);            

void setup() {
  // set the speed at 60 rpm: 
  myStepper.setSpeed(stepSpeed);
  // initialize the serial port:
  Serial.begin(9600);
  Serial.setTimeout(serialTimeout);
}

void loop() {
  while (!Serial.available()); // Listen to serial input
  char serbuf[8] = ""; // Reinitialise buffer (8 bytes)
  Serial.readBytesUntil(' ', serbuf, 8); // Until whitespace
  // Obtain which input command (enumerated)
  int enumc = -1; // default choice
  int maxChoice = 4;
  char sercmd[maxChoice][8] = {"HELP", "ONEREV", "SETANG", "RESET"};
  for (int c=0; c<maxChoice; c++){
    if (strcasecmp(sercmd[c],serbuf) == 0){ 
      enumc = c;// Obtain match
    }
  }
  // Declaring some other parameters
  char resbuf[4] = "";
  int angleTarget;
  // Switching between different cases
  switch(enumc){
    case 0: //HELP
      Serial.print("Stepper Motor Implementation Level 1\n");
      Serial.print("HELP       Print help statement\n");
      Serial.print("ONEREV     Perform one revolution\n");
      Serial.print("SETANG X   Set angle to be X degrees\n");
      Serial.print("RESET      Reset angle to zero degrees\n");
      break; 
    case 1: //ONEREV
      oneRev(stepDirection);
      break;
    case 2: //SETANG
      // listen again (for angle)
      while (!Serial.available());
      Serial.readBytesUntil(' ', resbuf, 8); // Until whitespace
      angleTarget = atoi(resbuf);
      EEPROM_writeAnything(EEloc_angleTarget, angleTarget);
      moveStepper();
      break;
    case 3: //RESET
      Serial.print("RESET\n");
      angleTarget = 0; // reset to 0 degrees
      EEPROM_writeAnything(EEloc_angleTarget, angleTarget);
      moveStepper();
      break;
    default:
      Serial.print("Unknown command\n");
      break;
  }
}

int oneRev(int dir){
  // dir = 1 or -1
  for (int i=0; i<stepsPerRevolution; i++){
    myStepper.step(dir);
    delay(stepDelay);
  }
  return 1;
}

int moveStepper(){
  int current;
  int target;
  EEPROM_readAnything(EEloc_angleCurrent, current);
  EEPROM_readAnything(EEloc_angleTarget, target);
  double stepsDiff = (target - current) * (float) (stepsPerRevolution / 360.0);
  // Printing how many steps it moves.
  Serial.print("Moving ");
  Serial.println(stepsDiff);
  // Moving 
  int dir = checkSign(stepsDiff);
  for (long i=0; i<abs(stepsDiff); i++){
    myStepper.step(dir);
    delay(stepDelay);
  }
  // Current angle is now the target angle
  EEPROM_writeAnything(EEloc_angleCurrent, target);
  return 1;
}

int checkSign(double num){
  if (num > 0) return 1;
  if (num < 0) return -1;
  return 0;
}
