#include <Servo.h>
#include "DHT.h"
#define DHTPIN A5           // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11      //seting the type of senser that shon and me are using
DHT dht(DHTPIN, DHTTYPE);  // Initialize DHT sensor.
Servo axonServo;  // Create a servo object to control your Axon servo
int servoPin = 9; // Connect the yellow/white signal wire to Digital Pin 9
String msg = "";
unsigned long t = 0;
unsigned long tempT = 0;
int yes = 1;
#define mf 2  //m-motor  f-forword
#define mr 4  //m-motor  r-reverse
#define r1 5 //relay 1-5
#define r2 6 //relay 1-5
#define r3 7 //relay 1-5
#define r4 8 //relay 1-5

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
  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  pinMode(r3, OUTPUT);
  pinMode(r4, OUTPUT);
  dht.begin();  //starting the dht

  // Good practice: ensure the motor starts in a stopped state
  axonServo.write(0);
  digitalWrite(mr, LOW);
  digitalWrite(mf, LOW);
  axonServo.write(0);
}

void loop() {
  checkTemp();
  if ( Serial.available()) {
    msg = Serial.readStringUntil('\n');
    //Serial.println(msg);
    t = millis();
    if (msg == "open") {
      while (!Serial.available() && millis() - t < 1000) {
        delay(50);
      }
      if (millis() - t < 1000) {
        msg = Serial.readStringUntil('\n');
        actuateMechanism(msg.toInt(),1);}  //conversion of msg to int
    } else if (msg == "close") {
        while (!Serial.available() && millis() - t < 1000) {
          delay(50);
        }
        if (millis() - t < 2000) {
          msg = Serial.readStringUntil('\n');
          actuateMechanism(msg.toInt(), -1);}  //conversion of msg to int
    } else if (msg == "volt") {
          while (!Serial.available() && millis() - t < 2000) {
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
// dir: 1 to open, -1 to close
if (dir == 1){
  switch (num) { //angle devided by axon max (355) multiplied by .write func max (180)
    case 1: axonServo.write(23);  break; //actually 45
    case 2: axonServo.write(46);  break;
    case 3: axonServo.write(68);  break;
    case 4: axonServo.write(91);  break;
    case 5: axonServo.write(114); break;
    default:
      Serial.println("Error: Invalid slot number");
      return;
    }
    delay(1500);
  }
  //setting the relays to choose the correct motor
  digitalWrite(r1, (num >= 2) ? HIGH : LOW);
  digitalWrite(r2, (num >= 3) ? HIGH : LOW);
  digitalWrite(r3, (num >= 4) ? HIGH : LOW);
  digitalWrite(r4, (num >= 5) ? HIGH : LOW);

  //Close circuits
  if (num == 2) digitalWrite(r2, LOW);
  if (num == 3) digitalWrite(r3, LOW);
  if (num == 4) digitalWrite(r4, LOW);

  if (dir == 1) {
    // Open
    digitalWrite(mr, LOW);
    digitalWrite(mf, HIGH);
  } else if (dir == -1) {
    // Close sequence
    digitalWrite(mr, HIGH);
    digitalWrite(mf, LOW);
  }
  delay(2000);
  digitalWrite(mr, LOW);
  digitalWrite(mf, LOW);
  
  digitalWrite(r1, LOW);
  digitalWrite(r2, LOW);
  digitalWrite(r3, LOW);
  digitalWrite(r4, LOW);

  if (dir == -1) axonServo.write(0);
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
