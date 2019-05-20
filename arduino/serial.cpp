#include <Stepper.h>

int in1Pin = 8;
int in2Pin = 9;
int in3Pin = 10;
int in4Pin = 11;

int incomingByte;

Stepper motor(512, in1Pin, in2Pin, in3Pin, in4Pin); // Вращение вокруг оси

void setup()
{
    pinMode(in1Pin, OUTPUT);
    pinMode(in2Pin, OUTPUT);
    pinMode(in3Pin, OUTPUT);
    pinMode(in4Pin, OUTPUT);
    Serial.begin(9600);
    motor.setSpeed(40);
}

void loop()
{
    if (Serial.available() > 0) {
        incomingByte = Serial.parseInt();
        Serial.println(incomingByte);
        motor.step(incomingByte * 500);

    }
}