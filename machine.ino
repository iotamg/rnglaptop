String msg = "";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(!Serial.available()){ delay(50); }
  msg = Serial.readStringUntil('\n');
  Serial.print(msg);
  if


}
