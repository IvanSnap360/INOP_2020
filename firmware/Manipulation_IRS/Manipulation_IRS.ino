#include <ServoSmooth.h>
#include <math.h>
#include "config.h"
#include "sturcts.h"


ServoSmooth joint[JOINT_COUNT];

Robot BOT;

WORKSHOP WSHP;
PLAN plan;
CONSTRUCTION CONST;

Position POS;

int joint_degs[JOINT_COUNT];

unsigned long servo_timer = 0;
int servo_delay = 20;

void setup() 
{
    Serial.begin(9600);
    pins_init();
    BOT.initialization_led(ON);
    config_init();
    servo_init();
    BOT.initialization_led(OFF);
    to_home();
    // inverse_math(-300, -300, 0);
    // for(int i = 0; i < JOINT_COUNT; i++)
    // {
    //   Serial.println("JOINT_" + String(i) + ": " + String(joint_degs[i]));
    // }



    while (digitalRead(BOT.start_stop_button_pin) != ON)
    {
        delay(100);
    }
    
}


void loop() 
{
    if(millis() - servo_timer >= servo_delay)
    {
        servo_timer = millis();
        for (int i = 0; i < JOINT_COUNT; i++)
        {
           joint[i].tickManual(); 
        }
    }

   




}
void config_init()
{
    for(int i = 0; i < JOINT_COUNT; i++)
    {
        BOT.joint[i].indicator_pin = JOINT_INDICATOR_PIN[i];
        BOT.joint[i].motor_pin = JOINT_MOTOR_PIN[i];
        
        BOT.joint[i].lenth_mm = JOINT_LENTH_MM[i];
        
        BOT.joint[i].pos_max = JOINT_POS_MAX_DEGS[i];
        BOT.joint[i].pos_min = JOINT_POS_MIN_DEGS[i];
        BOT.joint[i].pos_home = JOINT_POS_HOME_DEGS[i];

        BOT.joint[i].motor_speed = JOINT_SPEED[i];
        BOT.joint[i].motor_accel = JOINT_ACCEL[i];
        delay(10);
    }
}
void servo_init()
{
    for (int i = 0; i < JOINT_COUNT; i++)
    {
        joint[i].attach(BOT.joint[i].motor_pin, BOT.joint[i].pos_min, BOT.joint[i].pos_max);
        joint[i].setSpeed(BOT.joint[i].motor_speed);
        joint[i].setAccel(BOT.joint[i].motor_accel);
        delay(10);
    }
}

void to_home()
{
    for (int i = 0; i < JOINT_COUNT; i++)
    {
        go_servo_home(i);
        delay(100);
    }
}

void inverse_math(double _x_, double _y_, double _z_)
{
    double L1, L2, L3, q1, q2, q3, uA, uB, uC, uZ;
    L1 = JOINT_1_LENTH_MM;
    L2 = JOINT_2_LENTH_MM;

    L3 = hypot(_x_, _y_); 
    
    //sqrt(sq(L2) + sq(L1) - 2 * L2 * L1 * cos)

    q1 = degrees(atan2(_y_, _x_));
    q2 = degrees(acos((sq(L3) + sq(L1) - sq(L2)) / (2 * L3 * L1)));

    uA = q1 + q2;

    uB = degrees(acos((sq(L2) + sq(L1) - sq(L3)) / (2 * L2 * L1)));

    q3 = degrees(acos((sq(L3) + sq(L2) - sq(L1)) / (2 * L3 * L2)));

    if(GRIPPER_MODE == GRIPPER_MODE_GORIZONTAL)
    {
        uC = 180 - q3;
    }
    else if (GRIPPER_MODE == GRIPPER_MODE_VERTICAL)
    {
        uC = 90 + q3;
    }

    uZ = degrees(atan2(_z_, _x_));


    joint_degs[JOINT_0_ID] = round(uZ);
    joint_degs[JOINT_1_ID] = round(uA);
    joint_degs[JOINT_2_ID] = round(uB);
    joint_degs[JOINT_3_ID] = round(uC);

}
/*
void forward_math(double uA, double uB, double Uc, double Uz)
{
    double XA = JOINT_1_LENTH_MM * cos(radians(uA));
    double YA = JOINT_1_LENTH_MM * sin(radians(uA));

    double XB = JOINT_2_LENTH_MM * cos(radians(uA) + radians(uB));
    double YB = JOINT_2_LENTH_MM * sin(radians(uA) + radians(uB));

    double XC
}
*/

void go_servo_home(int _id)
{   
    joint[_id].write(BOT.joint[_id].pos_home);
    joint[_id].setTargetDeg(BOT.joint[_id].pos_home);
    BOT.joint[_id].set_indicator(ON);
}

void pins_init()
{
    for(int i = 0; i < JOINT_COUNT; i++)
    {
        pinMode(BOT.joint[i].motor_pin, OUTPUT);
        pinMode(BOT.joint[i].indicator_pin, OUTPUT);
    }
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(INIT_LED_PIN, OUTPUT);
}
void update_servo()
{
    for(int i = 0; i < JOINT_COUNT - 1; i++)
    {
        joint[i].write(joint_degs[i]);
        joint[i].setTargetDeg(joint_degs[i]);
    }
}
