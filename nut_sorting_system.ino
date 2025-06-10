#include <LiquidCrystal.h>
#include <Servo.h>

// Pin Definitions
#define IR_SENSOR 4
#define MOTOR_FWD 7
#define MOTOR_BWD A1

// Objects
LiquidCrystal lcd(13, 12, 11, 10, 9, 8);
Servo servoA;
Servo servoB;
Servo servoC;

// Global Variables
char dataFromPython;

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);

  pinMode(IR_SENSOR, INPUT);
  pinMode(MOTOR_FWD, OUTPUT);
  pinMode(MOTOR_BWD, OUTPUT);

  servoA.attach(3);
  servoB.attach(5);
  servoC.attach(6);

  digitalWrite(MOTOR_FWD, HIGH);
  digitalWrite(MOTOR_BWD, LOW);

  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print("Nut's Filter");
  delay(2000);
}

void loop() {
  sortingSystem();
}

void sortingSystem() {
  if (digitalRead(IR_SENSOR) == LOW) {
    digitalWrite(MOTOR_FWD, LOW);
    digitalWrite(MOTOR_BWD, LOW);

    if (Serial.available() > 0) {
      dataFromPython = Serial.read();
      executeSorting(dataFromPython);
    }
  } else {
    digitalWrite(MOTOR_FWD, HIGH);
    digitalWrite(MOTOR_BWD, LOW);
  }
}

void executeSorting(char category) {
  switch (category) {
    case 'A':
      displayMessage("First Class");
      moveServo(servoA);
      break;
    case 'B':
      displayMessage("Second Class");
      moveServo(servoB);
      break;
    case 'C':
      displayMessage("Third Class");
      moveServo(servoC);
      break;
    default:
      displayMessage("Invalid Input");
      break;
  }
}

void displayMessage(const char* message) {
  digitalWrite(MOTOR_FWD, HIGH);
  digitalWrite(MOTOR_BWD, LOW);
  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print(message);
}

void moveServo(Servo &servoMotor) {
  servoMotor.write(180);
  delay(500);
  servoMotor.write(0);
  delay(500);
}
