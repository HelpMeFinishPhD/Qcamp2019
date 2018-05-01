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
    
// initialize the IR library
IRsend irsend;         

void setup() {
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
  int maxChoice = 5;
  char sercmd[maxChoice][8] = {"HELP", "SBLINK", "CBLINK", "SEND", "RECV"};
  for (int c=0; c<maxChoice; c++){
    if (strcasecmp(sercmd[c],serbuf) == 0){ 
      enumc = c;// Obtain match
    }
  }
  // Declaring some other parameters
  //-- none --
  
  // Switching between different cases
  switch(enumc){
    case 0: //HELP
      Serial.print("Stepper Motor Implementation Level 1\n");
      Serial.print("HELP       Print help statement\n");
      Serial.print("ONEREV     Perform one revolution\n");
      Serial.print("SETANG X   Set angle to be X degrees\n");
      Serial.print("RESET      Reset angle to zero degrees\n");
      break; 
    case 1: //RESET
      Serial.print("RESET\n");
      angleTarget = 0; // reset to 0 degrees
      EEPROM_writeAnything(EEloc_angleTarget, angleTarget);
      moveStepper();
      break;
    case 2: //SETANG
      // listen again (for angle)
      while (!Serial.available());
      Serial.readBytesUntil(' ', valbuf, 8); // Until whitespace
      angleTarget = atoi(valbuf);
      EEPROM_writeAnything(EEloc_angleTarget, angleTarget);
      moveStepper();
      break;
    case 3: //SETPOL
      while (!Serial.available());
      Serial.readBytesUntil(' ', valbuf, 8); // Until whitespace
      int setPolTo; 
      setPolTo = (int)valbuf[0] - 48; // Only convert the first char: the rest are bullshit
      if (setPolTo < 0 || setPolTo > 3){
        Serial.println("Input error detected.");
        setPolTo = 0; // If input error, assume zero polarisation (H)
      }
      angleTarget = setPolTo * 45 + polOffset;
      EEPROM_writeAnything(EEloc_angleTarget, angleTarget);
      moveStepper();
      break;
    case 4: //POLOFF
      while (!Serial.available());
      Serial.readBytesUntil(' ', valbuf, 8); // Until whitespace
      polOffset = atoi(valbuf);
      EEPROM_writeAnything(EEloc_polOffset, polOffset);
      Serial.print("Polarisation offset: ");
      Serial.println(polOffset);
      break;
    case 5: //POLSEQ
      while (!Serial.available());
      Serial.readBytesUntil(' ', polseqbuf, seqLength);     
      polBuffToSeq(polseqbuf, seqLength, polSeq);
      // Debug for printing purposes 
      for (int i=0; i<seqLength; i++){
        Serial.print(polSeq[i]);
      } Serial.print('\n');
      // Debug endline
      break;  
    case 6: //STSEQ
      // Go to initial polarisation
      angleTarget = seqInitTarget * 45 + polOffset;
      EEPROM_writeAnything(EEloc_angleTarget, angleTarget);
      moveStepper();
      // Look at the time now
      unsigned long timeNow;
      unsigned long timeNext;
      timeNext = millis();
      for (int i=0; i<seqLength; i++){
        // Wait for the next time step
        timeNow = millis();
        while(timeNow<timeNext){
          timeNow = millis();}; // Wait till next time step
        // Perform commands
        angleTarget = polSeq[i] * 45 + polOffset;
        EEPROM_writeAnything(EEloc_angleTarget, angleTarget);
        moveStepper();
        // Switch on laser 
        laserOn(timeNext);
        timeNext += seqTimeStep; // Increase time step
      }
      // Go back to initial polarisation
      angleTarget = seqInitTarget * 45 + polOffset;
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
  // Debug: Printing how many steps it moves.
  // Serial.print("Moving ");
  // Serial.println(stepsDiff);
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

int polBuffToSeq(char polseqbuf[], int seqLength, int polSeq[]){
  // This mani-fold thingy is to implement an efficient rotation, such that
  // the maximum rotation per sequence step is not more than 2 (90 degrees)
  int mani = 4; // Group size of 4 (H,D,V,A)
  int fold = 0; // Starting from 0 to 3;
  for(int i=0; i<seqLength; i++){
    // Spit error message if the input value is erratic
    int polnow = (int)polseqbuf[i] - 48; // ASCII to int
    // Convert all nulls to zero ints (if sequences less than 64 digits)
    if (polnow == -48) polnow = 0;
    if (polnow < 0 || polnow > 3){
      Serial.println("Input error detected.");
      polnow = 0; // Skipping the input
    }
    // Constructing the polSeq array
    polSeq[i] = polnow + mani * fold;
    // Increase manifold if 3 -> 0, and decrease manifold if 0 -> 3.
    if (i<seqLength-1){  // Skipping last value comparison
      int polnext = (int)polseqbuf[i+1] - 48; 
      if (polnow==3 && polnext==0){
        fold += 1;
      }
      if (polnow==0 && polnext==3){
        fold -= 1;
      }
    }
  }
  return 1;
}

int laserOn(unsigned long timeStep){
  unsigned long timeNow = 0;
  // Wait until the start trigger
  while(timeNow<timeStep+seqLsrStart){
    timeNow = millis();};
  Serial.println(timeNow-timeStep);
  digitalWrite(pinLsr, HIGH);
  // Wait until the stop trigger
  while(timeNow<timeStep+seqLsrStop){
    timeNow = millis();};
  digitalWrite(pinLsr, LOW);
  return 1;
}

