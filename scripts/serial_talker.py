import serial
import time
import argparse
import struct

"""
typedef struct 
{
    float motor_l_cmd;
    float motor_r_cmd;
    uint16_t servo_cmd_deg;
    uint32_t checksum;
} serial_decryption_t;
"""


class SerialCommander:
    def __init__(self, port, baudrate, debug=False):
        self.ser = serial.Serial(port, baudrate)
        self.ser.flushInput()
        self.ser.flushOutput()

        self.debug = debug

        time.sleep(1) # arduino resets itself into bootloader, this is a workaround

    def write_raw(self, data):
        if self.debug:
            print(f"Writing: {data}")
        self.ser.write(data)

    def write(self, motor_l_cmd, motor_r_cmd, servo_cmd_deg):
        # Clamp the motor commands to -1 to 1
        motor_l_cmd = max(-1, min(1, motor_l_cmd))
        motor_r_cmd = max(-1, min(1, motor_r_cmd))

        # Clamp the servo command to 0 to 180
        servo_cmd_deg = int(max(0, min(180, servo_cmd_deg)))

        # Define the struct format: '<ffH' for motor_l_cmd, motor_r_cmd, and servo_cmd_deg
        struct_format = '<ffH'

        # Pack the data into a byte array
        packed_data = struct.pack(
            struct_format,
            motor_l_cmd,
            motor_r_cmd,
            servo_cmd_deg
        )

        # Calculate checksum
        checksum = sum(packed_data) & 0xFFFFFFFF  # Ensure checksum fits in 4 bytes

        # Append checksum to the packed data
        packed_data_with_checksum = packed_data + struct.pack('<I', checksum)

        # Write the data
        if self.debug:
            print(f"Writing speeds: {motor_l_cmd}, {motor_r_cmd}, servo angle: {servo_cmd_deg}")
        self.write_raw(packed_data_with_checksum)

    def read_serial_output(self):
        while self.ser.in_waiting > 0:
            # Read the serial output
            serial_output = self.ser.readline().decode('utf-8').strip()

            # Print the serial output
            print(f"Serial output: {serial_output}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, default='/dev/ttyACM0')
    parser.add_argument('--baudrate', type=int, default=921600)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--virtual', action='store_true')
    args = parser.parse_args()

    if args.virtual:
        # make a fake serial port
        import pty
        import os
        master, slave = pty.openpty()
        slave_name = os.ttyname(slave)
        print(f"Virtual serial port created: {slave_name}")
        args.port = slave_name

    commander = SerialCommander(args.port, args.baudrate, debug=args.debug)

    while True:
        motor_l_cmd = float(input("Enter motor l cmd: "))
        motor_r_cmd = float(input("Enter motor r cmd: "))
        servo_cmd_deg = float(input("Enter servo cmd deg: "))

        commander.write(motor_l_cmd, motor_r_cmd, servo_cmd_deg)

        time.sleep(0.2)  # Wait briefly for the microcontroller to respond
        commander.read_serial_output()  # Read and print the serial output

        if args.virtual:
            # read from the virtual port
            print(os.read(master, 1000))
        