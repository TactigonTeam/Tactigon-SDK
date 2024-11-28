
#include <Servo.h>
#include <BraccioRobot.h>

#define END_CHAR          0x7C  //|
#define INPUT_BUFFER_SIZE 50

static char inputBuffer[INPUT_BUFFER_SIZE];
Position armPosition;

// SoftwareSerial debugSerial(10,11);

void setup() {
  Serial.begin(115200);
  //debugSerial.begin(115200);
  BraccioRobot.init();
}

void loop() {
    handleInput();
}

void handleInput() {
  if (Serial.available() > 0){
    byte result = Serial.readBytesUntil(END_CHAR, inputBuffer, INPUT_BUFFER_SIZE);
    inputBuffer[result] = 0;
    interpretCommand(inputBuffer);
    /*
    char inByte = Serial.read();
    
    if (inByte != END_CHAR && (message_pos < INPUT_BUFFER_SIZE - 1)){
      message[message_pos] = inByte;
      message_pos ++;   
    } else {
      debugSerial.print(message);
      delay(5000);
      // interpretCommand(message);
    }
    */
  }
  delay(100);
  /*
  if (Serial.available() > 0) {
    // byte result = Serial.readBytesUntil('\n', inputBuffer, INPUT_BUFFER_SIZE);
    byte result = Serial.readBytesUntil('|', inputBuffer, INPUT_BUFFER_SIZE);
    inputBuffer[result] = 0;
    interpretCommand(inputBuffer, result);
  }
  */
}

void interpretCommand(char* inputBuffer) {
  if (inputBuffer[0] == 'P') {
    positionArm(&inputBuffer[0]);
  } else if (inputBuffer[0] == 'H') {
    homePositionArm();
  } else if (inputBuffer[0] == '0') {
    BraccioRobot.powerOff();
    Serial.print(0); // OK
  }  else if (inputBuffer[0] == '1') {
    BraccioRobot.powerOn();
    Serial.print(0); // OK
  } else {
    Serial.print(1); //E0
  }
}

void positionArm(char *in) {
  int speed = armPosition.setFromString(in);
  speed = 200;
  if (speed > 0) {
    BraccioRobot.moveToPosition(armPosition, speed);
    Serial.print(0); // OK
  } else {
    Serial.print(2); // E1
  }
}

void homePositionArm() {
  BraccioRobot.moveToPosition(armPosition.set(90, 90, 90, 90, 90, 73), 150);
  Serial.print(0); // OK
}

/*
void interpretCommand(char* inputBuffer, byte commandLength) {
  if (inputBuffer[0] == 'P') {
    positionArm(&inputBuffer[0]);
  } else if (inputBuffer[0] == 'H') {
    homePositionArm();
  } else if (inputBuffer[0] == '0') {
    BraccioRobot.powerOff();
    Serial.write(0); // OK
  }  else if (inputBuffer[0] == '1') {
    BraccioRobot.powerOn();
    // Serial.write("OK");
    Serial.write(0);
  } else {
    Serial.write(1); //E0
  }
  Serial.flush();
}
*/
