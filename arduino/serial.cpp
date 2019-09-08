#include <Stepper.h>

int in1Pin = 8;
int in2Pin = 9;
int in3Pin = 10;
int in4Pin = 11;

int incomingByte;

Stepper motor(512, in1Pin, in2Pin, in3Pin, in4Pin); // Âðàùåíèå âîêðóã îñè

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

/*
const int line_sensor = 1; 
 
void setup() {
  Serial.begin(9600); // инициализация Serial-порта
 
}
 
void loop() {
  bool isLine = digitalRead(line_sensor); 
  if (isLine) { //если это линия, 
    Serial.println("There is line"); 
	// команды движения
  }
  else { // если линии нет
    Serial.println("There is no line"); // сообщить и об этом
  }
  delay(500); // задержка в 500 мс
}

*/
