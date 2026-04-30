#include "ACS712.h"
ACS712 ACS(A0, 5.0, 1023, 66);
void setup()
{
  Serial.begin(115200);
  while (!Serial);
  Serial.println();
  ACS.autoMidPoint();
  Serial.print("MidPoint: ");
  Serial.println(ACS.getMidPoint());
}
void loop()
{
  float A = ACS.mA_AC(50) / 1000.0;  
  if (A < 0.184) A*= 0;
  Serial.print("RMS Current: ");
  Serial.print(A, 3);
  Serial.println(" A");
  delay(1000);
}