#include <Stepper.h>

int in1Pin = 8;
int in2Pin = 9;
int in3Pin = 10;
int in4Pin = 11;

int in1Pin2 = 2;
int in2Pin2 = 3;
int in3Pin2 = 4;
int in4Pin2 = 5;
int incomingByte;

Stepper motor(512, in1Pin, in2Pin, in3Pin, in4Pin); // Вращение вокруг оси
Stepper motor2(512, in1Pin2, in2Pin2, in3Pin2, in4Pin2); // Выдвижение

void setup()
{
    pinMode(in1Pin, OUTPUT);
    pinMode(in2Pin, OUTPUT);
    pinMode(in3Pin, OUTPUT);
    pinMode(in4Pin, OUTPUT);
    pinMode(in1Pin2, OUTPUT);
    pinMode(in2Pin2, OUTPUT);
    pinMode(in3Pin2, OUTPUT);
    pinMode(in4Pin2, OUTPUT);
    Serial.begin(9600);
    motor.setSpeed(40);
    motor2.setSpeed(40);
}

void loop()
{
    if (Serial.available() > 0) {
        incomingByte = Serial.parseInt();
        Serial.println(incomingByte);
        motor.step(incomingByte * 500);
        motor2.step(incomingByte * 200);
    }
}