/*
  Generates 50 random number from 0 to 9 with Entropy
  Author: Qcamp (2018) 
*/

#include <Entropy.h>

// Parameter
const int seqLength = 50;
int randomArr[seqLength] = {}; 

void setup(){
  Serial.begin(9600);
  Serial.println("Generating numbers...");
  Entropy.initialize();
  specialRandom(randomArr, seqLength, 10);
  printSeq();
}

void loop(){
  // Pass
}

int printSeq(){
  // Print the stored sequence (values only from 0 to 3)
  for (int i=0; i<seqLength; i++){
    Serial.print(randomArr[i]); 
  } 
  Serial.print('\n'); // endline
  
  return 1; // Exits 
}

int specialRandom(int array[], int arrayLength, int maxVal){
  // Fill in the array with specialised random numbers in [0, maxVal)   
  for(int i=0; i<arrayLength; i++){
    array[i] = Entropy.random(maxVal);     
  }
}
