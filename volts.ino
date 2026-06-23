#include "ACS712.h"
ACS712 C1(A0, 5.0, 1023, 66);
ACS712 C2(A1, 5.0, 1023, 66);
ACS712 C3(A2, 5.0, 1023, 66);
ACS712 C4(A3, 5.0, 1023, 66);
ACS712 C5(A4, 5.0, 1023, 66);
ACS712 sensors[] = {ACS712(A0, 5.0, 1023, 66),
  ACS712(A1, 5.0, 1023, 66),
  ACS712(A2, 5.0, 1023, 66),
  ACS712(A3, 5.0, 1023, 66),
  ACS712(A4, 5.0, 1023, 66), 
};
float A = 0;
void setup()
{
  Serial.begin(115200);
  while (!Serial);
}
void loop()
{
  for (int i = 0; i < 5; i+=1){
    Serial.print("Pc number:");
    Serial.print(i + 1);
    A = sensors[i].mA_AC(50) / 1000.0;  
    if (A < 0.184) A = 0;
    if (A = 0) Serial.println("Current charge is 100%");
    else if (A < 1.1) Serial.println("Current charge is above 75% (under 100%)");
    else Serial.println("Current charge is under 75%");
    delay(100);
  }
}