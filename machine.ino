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
#define r1 5//realy 1-5
#define r2 6//realy 1-5
#define r3 7//realy 1-5
#define r4 8//realy 1-5

#define f 13//fans
float idealTemp = 24; //temp we want
void setup() {
  Serial.begin(9600);
  // Attach the servo on pin 9 to the servo object
  axonServo.attach(servoPin);
  pinMode(f,OUTPUT);
  pinMode(mf, OUTPUT);
  pinMode(mf, OUTPUT);
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
    Serial.print(msg);
    t = millis();
    if (msg == "open") {
      t = millis();
      while (!Serial.available() && millis() - t < 1000) {
        delay(50);
      }
      if (millis() - t < 1000) {
        msg = Serial.readStringUntil('\n');
        if (msg.startsWith("open")) {
          int n = msg.substring(msg.indexOf("open") + String("open").length(), msg.indexOf("open") + String("open").length() + 1).toInt();
          open(n);
        } else if (msg.startsWith("close")) {
          int n = msg.substring(msg.indexOf("close") + String("close").length(), msg.indexOf("close") + String("close").length() + 1).toInt();
          close(n);
        } else if (msg.startsWith("volt")) {
          int n = msg.substring(msg.indexOf("volt") + String("volt").length(), msg.indexOf("volt") + String("volt").length() + 1).toInt();
          Serial.print(voltege(n));
        }
        //Serial.print("Opening PC: ");
        //Serial.println(msg);
        //enter open code for pc number 'msg'
        //wait up to 5 seconds then lock and return
        //return if pc is there
        Serial.write("True");
        //Serial.println("False")
      }
    }
  }
  else delay(50);
}
void checkTemp(){
    if (tempT - millis() > 2000) {
    if ( dht.readTemperature(false) > idealTemp)
      digitalWrite(f,HIGH);
    else 
      digitalWrite(f,LOW);
    tempT = millis();
  }
}

void close(int num) {

  switch (num) {
    case 1:
      axonServo.write(22);
      delay(2000);
      digitalWrite(r1, LOW);
      digitalWrite(mr, LOW);
      digitalWrite(mf, HIGH);
      break;
    case 2:
      axonServo.write(45);
      delay(2000);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, LOW);
      digitalWrite(mr, LOW);
      digitalWrite(mf, HIGH);
      break;
    case 3:
      axonServo.write(67);
      delay(2000);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, LOW);
      digitalWrite(mr, LOW);
      digitalWrite(mf, HIGH);
      break;
    case 4:
      axonServo.write(90);
      delay(2000);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, HIGH);
      digitalWrite(r4, LOW);
      digitalWrite(mr, LOW);
      digitalWrite(mf, HIGH);
      break;
    case 5:
      axonServo.write(112);
      delay(2000);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, HIGH);
      digitalWrite(r4, HIGH);
      digitalWrite(mr, LOW);
      digitalWrite(mf, HIGH);
      break;
    default:
      Serial.print("somthing wrong");
      break;

  }
  delay(3000);
  axonServo.write(0);
  digitalWrite(mr, LOW);
  digitalWrite(mf, LOW);
}


void open(int num) {

  switch (num) {
    case 1:
      axonServo.write(22);
      delay(2000);
      digitalWrite(r1, LOW);
      digitalWrite(mr, HIGH);
      digitalWrite(mf, LOW);
      break;
    case 2:
      axonServo.write(45);
      delay(2000);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, LOW);
      digitalWrite(mr, HIGH);
      digitalWrite(mf, LOW);
      break;
    case 3:
      axonServo.write(67);
      delay(2000);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, LOW);
      digitalWrite(mr, HIGH);
      digitalWrite(mf, LOW);
      break;
    case 4:
      axonServo.write(90);
      delay(2000);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, HIGH);
      digitalWrite(r4, LOW);
      digitalWrite(mr, HIGH);
      digitalWrite(mf, LOW);
      break;
    case 5:
      axonServo.write(112);
      delay(2000);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, HIGH);
      digitalWrite(r4, HIGH);
      digitalWrite(mr, HIGH);
      digitalWrite(mf, LOW);
      break;
    default:
      Serial.print("somthing wrong");
      break;

  }
  delay(3000);
  axonServo.write(0);
  digitalWrite(mr, LOW);
  digitalWrite(mf, LOW);
}

double voltege(int num){
  return 5;
}
