String msg = "";
int time = 0;
int yes = 1;
#define m1f 3  //m-motor 1-num of motor f-forword
#define m1r 4  //m-motor 1-num of motor r-reverse
#define m2f 5
#define m2r 6
#define m3f
#define m3r
#define m4f
#define m4r
#define m5f
#define m5r
#define mainf 10 //main motor forword
#define mainr 11 //main motor backwords
void setup() {
  // put your setup code here, to run once:
  pinMode(m1f, OUTPUT);
  pinMode(m2f, OUTPUT);
  pinMode(m1f, OUTPUT);
  pinMode(m2f, OUTPUT);
  pinMode(mainf, OUTPUT);
  pinMode(mainf, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (!Serial.available()) { delay(50); }
  msg = Serial.readStringUntil('\n');
  Serial.print(msg);
  time = millis();
  if (msg == "open") {
    time = millis();
    while (!Serial.available() && millis() - time < 1000) { delay(50); }
    if (millis() - time < 1000) {
      msg = Serial.readStringUntil('\n');
      if (msg.startsWith("open")) {
        int n=msg.substring(msg.indexOf("open")+String("open").length(),msg.indexOf("open")+String("open").length()+1).toInt();
        open(n);
      } else if (msg.startsWith("close")) {
        int n=msg.substring(msg.indexOf("close")+String("close").length(),msg.indexOf("close")+String("close").length()+1).toInt();
        close(n);
      } else if (msg.startsWith("volt")) {
        Serial.print(voltege());
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

void close(int num) {
  digitalWrite(mainf, HIGH);
  digitalWrite(mainr, LOW);
  delay(100);
  digitalWrite(mainf, LOW);
  digitalWrite(mainr, LOW);
  switch (num) {
    case 1:
      digitalWrite(m1f, HIGH);
      digitalWrite(m1r, LOW);
      delay(100);
      digitalWrite(m1f, LOW);
      digitalWrite(m1r, LOW);
      break;
    case 2:
      digitalWrite(m2f, HIGH);
      digitalWrite(m2r, LOW);
      delay(100);
      digitalWrite(m2f, LOW);
      digitalWrite(m2r, LOW);
      break;
    default:
      Serial.print("somthing wrong");
  }
  digitalWrite(mainf, LOW);
  digitalWrite(mainr, HIGH);
  delay(100);
  digitalWrite(mainf, LOW);
  digitalWrite(mainr, LOW);
}

void open(int num) {
  digitalWrite(mainf, HIGH);
  digitalWrite(mainr, LOW);
  delay(100);
  digitalWrite(mainf, LOW);
  digitalWrite(mainr, LOW);
  switch (num) {
    case 1:
      digitalWrite(m1f, LOW);
      digitalWrite(m1r, HIGH);
      delay(100);
      digitalWrite(m1f, LOW);
      digitalWrite(m1r, LOW);
      break;
    case 2:
      digitalWrite(m2f, LOW);
      digitalWrite(m2r, HIGH);
      delay(100);
      digitalWrite(m2f, LOW);
      digitalWrite(m2r, LOW);
      break;
    default:
      Serial.print("somthing wrong");
  }
  digitalWrite(mainf, HIGH);
  digitalWrite(mainr, LOW);
  delay(100);
  digitalWrite(mainf, LOW);
  digitalWrite(mainr, LOW);
}

String voltege() {
  return "vol";
}