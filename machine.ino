String msg = "";
int time = 0;
int yes = 1;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(!Serial.available()){ delay(50); }
  msg = Serial.readStringUntil('\n');
  Serial.print(msg);
  time = millis();
  if (msg == "open"){
    time = millis();
    while(!Serial.available() && millis()- time < 1000){ delay(50); }
    if (millis()- time < 1000){
      msg = Serial.readStringUntil('\n');
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
