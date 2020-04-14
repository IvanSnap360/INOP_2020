#include "MeOrion.h"

MePort servoPort(PORT_3);
int pin_dir = mePort[PORT_1].s1;//the direction pin connect to Base Board PORT1 SLOT1
int pin_stp = mePort[PORT_1].s2;//the Step pin connect to Base Board PORT1 SLOT2
int pin_btn = A3;
int pin_irs = A2;
int pin_dwn = 8;
int pin_run = 2;
int pin_sr1 = servoPort.pin1();
int pin_sr2 = servoPort.pin2();

Servo sr1;
Servo sr2;
MeDCMotor motorUp(M1);

int currentPos;

void setup()
{
  Serial.begin(9600);
  Serial.println("Hello from robot!");
  pinMode(pin_dir, OUTPUT);
  pinMode(pin_stp, OUTPUT);
  pinMode(pin_dwn, INPUT_PULLUP);
  pinMode(pin_run, INPUT_PULLUP);

  sr1.attach(pin_sr1);
  sr2.attach(pin_sr2);

  raiseCube();
  home();
  unsigned long tt = millis();
  while(true) {
    if(millis() - tt > 1000) {
      Serial.println("Waiting...");
      tt = millis();
    }
    if(digitalRead(pin_dwn) == 0) {
      moveDown();
    }
    if(digitalRead(pin_run) == 0) {
      Serial.println("GO!");
      return;
    }
  }

  /*


  return;
  delay(1000);
  moveTo(4);
  takeCube2();
  moveUp();
  moveTo(1);
  //moveDown();
  raiseCube();
  */
}

void step(boolean dir,int steps, int speed)
{
  digitalWrite(pin_dir,dir);
  delay(1);
  for(int i=0;i<steps;i++)
  {
    digitalWrite(pin_stp, HIGH);
    delayMicroseconds(3000/speed);
    digitalWrite(pin_stp, LOW);
    delayMicroseconds(3000/speed); 
  }
}

void raiseCube() {
  sr1.write(90);
  sr2.write(90);
  delay(200);
}

void takeCube1() {
  sr1.write(10);
  sr2.write(170);
  delay(500);
}

void takeCube2() {
  sr1.write(180);
  sr2.write(0);
  delay(500);
}

void home() 
{
  while(analogRead(pin_btn) > 500)
    step(0, 100, 50);
  currentPos = 0;
}

void moveTo(int pos) 
{
  int moveSteps = (pos - currentPos) * 3500;
  if(moveSteps > 0)
    step(1, moveSteps, 100);
  else
    step(0, -moveSteps, 100);
  currentPos = pos;
}

void moveDown() 
{
  while(analogRead(pin_irs) > 100) {
    motorUp.run(255);
  }
  motorUp.run(255);
  delay(100);
  while(analogRead(pin_irs) < 100) {
    motorUp.run(255);
  }
  motorUp.stop();
}

void moveUp() 
{
  while(analogRead(pin_irs) > 100) {
    motorUp.run(-255);
  }
  motorUp.run(-255);
  delay(100);
  while(analogRead(pin_irs) < 100) {
    motorUp.run(-255);
  }
  motorUp.stop();
}

void loop()
{
  
  
  //home();
  //step(1,1000, 100);//run 200 step
  //delay(1000);
  //step(0,1000, 100);
  //delay(1000);
}
