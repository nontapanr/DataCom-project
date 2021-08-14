#include <Servo.h>
Servo myservo;

void setup() {
  Serial.begin(115200);
  myservo.attach(9);
}

int angle = 90;
//int state = 0;

void testReceive() {
  if (Serial.available() > 0) {
    char inByte = Serial.read();

    if (inByte == 'l' || inByte == 'L') {
      angle = 128;
    }
    if (inByte == 'r' || inByte == 'R') {
      angle = 51;
    }
    if (inByte == 'm' || inByte == 'M') {
      angle = 90;
    }
  }
  myservo.write(angle);
}


void loop() {
  testReceive();
  Serial.flush();
}
