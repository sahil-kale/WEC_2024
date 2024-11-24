#include "serial_decryption.hpp"
#include <string.h>
#include <Arduino.h>

#define SERIAL_DBG

bool decrypt_serial_data(const uint8_t *data, size_t len, serial_decryption_t *decrypted_data)
{
    bool ret = false;
    if (len == sizeof(serial_decryption_t))
    {
        memcpy(decrypted_data, data, len);

        // sum over all bytes of the struct
        uint32_t checksum = 0;
        const size_t length_to_check = len - sizeof(uint32_t);
        for (size_t i = 0; i < length_to_check; i++)
        {
            checksum += ((uint8_t *)decrypted_data)[i];
        }

        // check if the checksum is correct
        ret = checksum == decrypted_data->checksum;
        
        // consider kicking and screaming if the checksum is incorrect
    }

    return ret;
}