#include <Arduino.h>
#include <Servo.h>
#include "motors.h"

#define IN1 13
#define IN2 12
#define IN3 9
#define IN4 8

#define LEFT_MOTOR 11
#define RIGHT_MOTOR 5
#define SERVO_MOTOR 6
#define MAX_PWM 255

#define MAX_SERVO_PWM 2000
#define MIN_SERVO_PWM 1000
#define MAX_SERVO_ANGLE_DEG 180

Servo claw;

void setupMotors()
{
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(LEFT_MOTOR, OUTPUT);
    pinMode(RIGHT_MOTOR, OUTPUT);
    claw.attach(SERVO_MOTOR);
    claw.writeMicroseconds(MAX_SERVO_PWM);
}

void driveMotorCommand(float motor_l_cmd, float motor_r_cmd)
{
    // motor commands between -1 and 1 (inclusive)
    if(motor_l_cmd > 0)
    {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
    }
    else
    {
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
    }

    if(motor_r_cmd < 0)
    {
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
    }
    else
    {
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
    }

    analogWrite(LEFT_MOTOR, fabs(motor_l_cmd)*MAX_PWM);
    analogWrite(RIGHT_MOTOR, fabs(motor_r_cmd)*MAX_PWM);
}

void servoMotorCommand(uint16_t angle)
{
    if(angle > MAX_SERVO_ANGLE_DEG)
    {
        angle = MAX_SERVO_ANGLE_DEG;
    }
    else if (angle < 0)
    {
        angle = 0;
    }
    
    // angle is in degrees measured on the real servo
    claw.writeMicroseconds((float(angle)/MAX_SERVO_ANGLE_DEG)*(MAX_SERVO_PWM - MIN_SERVO_PWM) + MIN_SERVO_PWM);
}
