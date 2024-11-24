import pygame
import argparse
from pygame.locals import *
from serial_talker import SerialCommander

def main(args):
    if args.virtual:
        import pty
        import os
        master, slave = pty.openpty()
        slave_name = os.ttyname(slave)
        print(f"Virtual serial port created: {slave_name}")
        args.port = slave_name
    
    commander = SerialCommander(args.port, args.baudrate, debug=args.debug)

    
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    running = True

    speed = 0.1
    servo_angle_muliplier = 15
    servo_angle = 0

    cmd_speed_l = 0
    cmd_speed_r = 0

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                old_speed = speed
                if event.key == K_w:
                    cmd_speed_r = 1 * speed
                    cmd_speed_l = 1 * speed
                elif event.key == K_a:
                    cmd_speed_r = 1 * speed
                    cmd_speed_l = -1 * speed
                elif event.key == K_s:
                    cmd_speed_r = -1 * speed
                    cmd_speed_l = -1 * speed
                elif event.key == K_d:
                    cmd_speed_r = -1 * speed
                    cmd_speed_l = -1 * speed
                elif event.key == K_p:
                    servo_angle += 1 * servo_angle_muliplier
                elif event.key == K_o:
                    servo_angle -= 1 * servo_angle_muliplier
                elif event.key == K_UP:
                    speed += 0.1
                    # scale the speed to the new speed
                    cmd_speed_l = cmd_speed_l / old_speed * speed
                    cmd_speed_r = cmd_speed_r / old_speed * speed
                elif event.key == K_DOWN:
                    speed -= 0.1
                    # scale the speed to the new speed
                    cmd_speed_l = cmd_speed_l / old_speed * speed
                    cmd_speed_r = cmd_speed_r / old_speed * speed
            
                if args.debug:
                    print(f"Speed: {cmd_speed_l}, {cmd_speed_r}, Servo: {servo_angle}")
                commander.write(speed, speed, servo_angle)

    pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, default='/dev/ttyACM0')
    parser.add_argument('--baudrate', type=int, default=921600)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--virtual', action='store_true')
    args = parser.parse_args()

    main(args)

