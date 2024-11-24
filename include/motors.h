#include <Arduino.h>

void setupMotors();
void driveMotorCommand(float motor_l_cmd, float motor_r_cmd);
void servoMotorCommand(uint16_t angle);
