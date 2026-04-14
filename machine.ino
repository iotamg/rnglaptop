msg = "";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  while(!Serial.available()) {delay(100)}
  

}