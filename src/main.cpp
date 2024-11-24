#include <Arduino.h>
#include "serial_decryption.hpp"
#include "motors.h"

//#define DEBUG

void setup() {
    Serial.begin(921600);
	setupMotors();
}

void loop() {
    serial_decryption_t decrypted_data;

    if (Serial.available() >= static_cast<int>(sizeof(serial_decryption_t)))
    {
        uint8_t data[sizeof(serial_decryption_t)] = {0};
        Serial.readBytes(data, sizeof(serial_decryption_t));
        if (decrypt_serial_data(data, sizeof(serial_decryption_t), &decrypted_data))
        {

        }
        else
        {
            Serial.println("Checksum failed");

        }
            #ifdef DEBUG
            Serial.print("Motor L: ");
            Serial.print(decrypted_data.motor_l_cmd);
            Serial.print(" Motor R: ");
            Serial.print(decrypted_data.motor_r_cmd);
            Serial.print(" Servo: ");
            Serial.println(decrypted_data.servo_cmd_deg);
            Serial.print(" Checksum: ");
            Serial.println(decrypted_data.checksum);
            #endif
		driveMotorCommand(decrypted_data.motor_l_cmd, decrypted_data.motor_r_cmd);
		// servoMotorCommand(decrypted_data.servo_cmd_deg);
    }

}
