/**
 * This sketch shows the basic use of ArduinoRpc library
 * It starts from the Input Pullup Serial tutorial of Arduino documentation:
 *  https://www.arduino.cc/en/Tutorial/InputPullupSerial
 * But implements a different path in order to switch the led status.
 * Here the pull up resistor status (High or Low) changes trigger
 * a remote call (through the serial port) to the external program.
 * The external program, receives the "PRESSED"/"RELEASED" value and 
 * executes a call to "LedUpdate" in order to correctly switch On/Off 
 * the embedded led.
 */
#include <ArduinoSerialRpc.h>

const int inputPin = 2;
boolean actualState = false;
boolean buttonPressed = false;
int switchingCount = 0;

ArduinoSerialRpc rpc("Led Tutorial Sketch (www.mauxilium.it)");

void setup() {
  Serial.begin(9600);
  pinMode(inputPin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  
  rpc.registerArduinoFunction("LedUpdate", ledUpdate);
}

void serialEvent() {
  rpc.serialEventHandler();
}

String ledUpdate(String status) {
  switchingCount++;
  if (status == "ON") {
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }
  return String(switchingCount);
}

void loop() {
  if (digitalRead(inputPin) == LOW) {
    buttonPressed = true;
  } else {
    buttonPressed = false;
  }

  if (actualState != buttonPressed) {
    if (buttonPressed) {
      rpc.executeRemoteMethod("button", "PRESSED");
    } else {
      rpc.executeRemoteMethod("button", "RELEASED");
    }
    actualState = buttonPressed;
  }
}
