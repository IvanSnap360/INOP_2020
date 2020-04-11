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


unsigned long servo_timer = 0;
int servo_delay = 20;

void setup() 
{
    pins_init();
    BOT.initialization_led(ON);
    config_init();
    servo_init();
    BOT.initialization_led(OFF);
    to_home();

    



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

// void math(double _x, double _y, double _z)
// {
    // double L1, L2, L3, q1, q2, q3, uA, uB, uC;
    // L1 = JOINT_1_LENTH_MM;
    // L2 = JOINT_2_LENTH_MM;
// 
    // L3 = sqrt((cos(_x)^2) + sqr(sin(_y)));
    // q2 = arccos(sqr(L1) + sqr(L2) + sqr(L3)) / (2 * L1 * L3);
    // q1 = arccos(L3 / cos(_x));
    // uA = degs(q1+q2);
    // uB = arccos(sqr(L1) + sqr(L2) - sqr(L3)) / (2 * L2 * L1);
    // uC = 180 - ((arccos(sqr(L2) + sqr(L3) - sqr(L1)) / (2 * L2 * L1)) - (cos(_x) / L3) );
// }
// 
void go_servo_home(int _id)
{
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
