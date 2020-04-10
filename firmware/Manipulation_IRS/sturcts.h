#ifndef STRUCTS_H
#define STRUCTS_H
#include "config.h"

struct Position
{
    int x = 0;
    int y = 0;
    int z = 0;
};

struct Joint
{
    int id = 0;

    double lenth_mm = 0;

    int motor_pin = 0;
    int indicator_pin = 0;

    int pos_degs = 0;
    int pos_home = 0;
    int pos_max = 0;
    int pos_min = 0;

    int motor_speed = 0;
    double motor_accel = 0;

    void set_indicator(bool st = false)
    {
        digitalWrite(indicator_pin, st);
    }

};

struct Robot
{
    Joint joint[JOINT_COUNT];
    Position Pos[3];

    int start_stop_button_pin = START_STOP_BUTTON_PIN;
    
    void initialization_led(bool st = false)
    {
        digitalWrite(INIT_LED_PIN, st);
    }
};


struct Cell
{
    bool is_cube = false;
    int cube_color = 0;
    int cube_type = 0;
    int pos[3] = {0, 0, 0};
    int grip_deg = 0;
};

struct WORKSHOP
{
    Cell cell[WORKSHOP_SIZE_X][WORKSHOP_SIZE_Y];
};

struct PLAN
{
    Cell cell[PLAN_SIZE_X][PLAN_SIZE_Y];
};

struct  CONSTRUCTION
{
    Cell cell[BUILDING_SIZE_X][BUILDING_SIZE_Y];
};





#endif