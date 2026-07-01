#include <Servo.h>
#include "DHT.h"
#include "ACS712.h"
#define DHTPIN A5           // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11      //seting the type of senser that shon and me are using
DHT dht(DHTPIN, DHTTYPE);  // Initialize DHT sensor.
Servo axonServo;  // Create a servo object to control your Axon servo
int servoPin = 9; // Connect the yellow/white signal wire to Digital Pin 9
String msg = "";
unsigned long t = 0;
unsigned long tempT = 0;
unsigned long moveT = 0; //for timimng closure sequence
int yes = 1;
#define mf 4  //m-motor  f-forword
#define mr 2  //m-motor  r-reverse
#define rA 5 //relay A (1 and B)
#define rB 6 //relay B (2 and C)
#define rC 7 //relay C (3 and D)
#define rD 8 //relay D (4 and 5)
#define ms1 3 //motor switch (pc 1)
#define ms3 12 //motor switch (pc 3)
#define ms4 11 //motor switch (pc 4)
#define ms5 10 //motor switch (pc 5)

#define timeToMove 400 //time it takes to move the pin a whole way.

#define fans 13 //relay that controls fans

ACS712 currents[] = {ACS712(A0, 5.0, 1023, 66),
  ACS712(A1, 5.0, 1023, 66),
  ACS712(A2, 5.0, 1023, 66),
  ACS712(A3, 5.0, 1023, 66),
  ACS712(A4, 5.0, 1023, 66), 
};
float idealTemp = 24; //temp we want
void setup() {
  Serial.begin(9600);
  // Attach the servo on pin 9 to the servo object
  axonServo.attach(servoPin);
  pinMode(fans,OUTPUT);
  pinMode(mf, OUTPUT);
  pinMode(mr, OUTPUT);
  pinMode(rA, OUTPUT);
  pinMode(rB, OUTPUT);
  pinMode(rC, OUTPUT);
  pinMode(rD, OUTPUT);
  dht.begin();  //starting the dht

  // Good practice: ensure the motor starts in a stopped state
  axonServo.write(0);
  digitalWrite(mr, LOW);
  digitalWrite(mf, LOW);
  digitalWrite(rA, HIGH);
  digitalWrite(rB, HIGH);
  digitalWrite(rC, HIGH);
  digitalWrite(rD, HIGH);
}

void loop() {
  checkTemp();
  if ( Serial.available()) {
    Serial.println("in loop");
    msg = Serial.readStringUntil('\n');
    Serial.println(msg);
    t = millis();
    if (msg == "open") {
      //Serial.println("Opening");
      while (!Serial.available() && millis() - t < 1000) {
        delay(50);
        Serial.println("Waiting");
      }
      if (millis() - t < 1000) {
        msg = Serial.readStringUntil('\n');
        Serial.println(msg);
        actuateMechanism(msg.toInt(),1);}  //conversion of msg to int
      else Serial.println("Timeout");
    } else if (msg == "close") {
        while (!Serial.available() && millis() - t < 1000) {
          delay(50);
        }
        if (millis() - t < 2000) {
          msg = Serial.readStringUntil('\n');
          actuateMechanism(msg.toInt(), -1);}  //conversion of msg to int
    } else if (msg == "volt") {
          while (!Serial.available() && millis() - t < 1000) {
            delay(50);
          }
          if (millis() - t < 1000) {
            msg = Serial.readStringUntil('\n');
            Serial.println(voltage(msg.toInt()));
      }
    }
  }
  else delay(50);
}
void checkTemp(){
    if (millis() - tempT > 2000) {
      if ( dht.readTemperature() > idealTemp) digitalWrite(fans,HIGH); //giving ground to relay makes the relay go to NO (fans at NC)
      else digitalWrite(fans,LOW);
      tempT = millis();
    }
}

void actuateMechanism(int num, int dir) {
// Serial.print("AM. PC: ");
// Serial.print(num);
// Serial.print(". dir: ");
// Serial.println(dir);
// dir: 1 to open, -1 to close
if (dir == 1){
  if (num > 0 && num < 6) axonServo.write(map(num*45,0,355,0,180)); //each position is 45 degrees apart. mapped to the max value 180 (which is actually moves 355)
  else  {
    Serial.println("Error: Invalid slot number");
    return;}
  delay(2500);
  }
  //setting the relays to choose the correct motor
  digitalWrite(rA, (num >= 2) ? LOW : HIGH);
  digitalWrite(rB, (num >= 3) ? LOW : HIGH);
  digitalWrite(rC, (num >= 4) ? LOW : HIGH);
  digitalWrite(rD, (num >= 5) ? LOW : HIGH);

  if (dir == 1) {
    // Open
    digitalWrite(mr, LOW);
    digitalWrite(mf, HIGH);
    delay(timeToMove);
  } else if (dir == -1) {
    // Close
    digitalWrite(mr, HIGH);
    digitalWrite(mf, LOW);
    moveT = millis();
    while (millis() - moveT < timeToMove || !checkMotor(num)) delay(50); //if it hasent touched and not enough time -> wait.
  }
  digitalWrite(mr, LOW);
  digitalWrite(mf, LOW);
  
  digitalWrite(rA, HIGH);
  digitalWrite(rB, HIGH);
  digitalWrite(rC, HIGH);
  digitalWrite(rD, HIGH);

  if (dir == -1) axonServo.write(0);
}

bool checkMotor(int pc){
  //true if touched the switch. else false
  switch (pc){
    case 1: return digitalRead(ms1);
    case 2: return false;
    case 3: return digitalRead(ms3);
    case 4: return digitalRead(ms4);
    case 5: return digitalRead(ms5);
  }
}
int voltage(int pc){
  float cu = currents[pc - 1].mA_AC(50); //milliamperes
  //100% is under 184mA
  //75%+ is under 1100mA
  //75%- is 1.1mA
  if (cu < 184) return 100;
  if (cu < 1100) return map(cu, 1100, 184, 75, 100);
  return 0; //doesnt matter, under 75% we cant distinguish.
}