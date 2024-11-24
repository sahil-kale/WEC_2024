#ifndef SERIAL_DECRYPTION_HPP
#define SERIAL_DECRYPTION_HPP

#include <stdint.h>
#include <stddef.h>

typedef struct __attribute__((packed))
{
    float motor_l_cmd;
    float motor_r_cmd;
    uint16_t servo_cmd_deg;
    uint32_t checksum;
} serial_decryption_t;

/**
 * @brief Decrypts the serial data
 * 
 * @param data The data to decrypt
 * @param len The length of the data
 * 
 * @return true if the data was decrypted successfully, false otherwise
 */
bool decrypt_serial_data(const uint8_t *data, size_t len, serial_decryption_t *decrypted_data);


#endif // SERIAL_DECRYPTION_HPP