#include <Arduino.h>

void setupMotors();
void driveMotorCommand(float motor_l_cmd, float motor_r_cmd, uint8_t delay_ms);
void servoMotorCommand(uint16_t angle);
