# ----------------------------------------------------------------------------- #
#                                                                               #                                                                          
#    Project:        Clawbot Controller with Events                             #
#    Module:         main.py                                                    #
#    Author:         VEX                                                        #
#    Created:        Fri Aug 05 2022                                            #
#    Description:    This example will use Controller button events to          # 
#                    control the V5 Clawbot arm and claw                        #
#                                                                               #                                                                          
#    Configuration:  V5 Clawbot (Individual Motors)                             #
#                    Controller                                                 #
#                    Claw Motor in Port 3                                       #
#                    Arm Motor in Port 8                                        #
#                    Left Motor in Port 1                                       #
#                    Right Motor in Port 10                                     #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

# Library imports
from vex import *

THRESHOLD = 3

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)

left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
drive_left = MotorGroup(left_motor_a, left_motor_b)

right_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
right_motor_b = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
drive_right = MotorGroup(right_motor_a, right_motor_b)

drivetrain = DriveTrain(drive_left, drive_right, 339.1, 350, 230, MM)

grabber = DigitalOut(brain.three_wire_port.a)
isGrabbing = False
grabber.set(isGrabbing)

wait(30, MSEC)

# define variables used for controlling motors based on controller inputs
left_to_be_stopped = False
right_to_be_stopped = False



def remote_control():
    global left_to_be_stopped, right_to_be_stopped
    while True:

        drivetrain_left_speed = controller_1.axis4.position() * 0.75 - controller_1.axis2.position()
        drivetrain_right_speed = controller_1.axis4.position() * 0.75 + controller_1.axis2.position()


        if drivetrain_left_speed < THRESHOLD and drivetrain_left_speed > -THRESHOLD:
                # check if the left motor has already been stopped
                if left_to_be_stopped:
                    # stop the left drive motor
                    drive_left.stop()
                    # tell the code that the left motor has been stopped
                    left_to_be_stopped = False
                else:
                    # reset the toggle so that the deadband code knows to stop the left motor next
                    # time the input is in the deadband range
                    left_to_be_stopped = True

        if drivetrain_right_speed < THRESHOLD and drivetrain_right_speed > -THRESHOLD:
                # check if the right motor has already been stopped
                if right_to_be_stopped:
                    # stop the right drive motor
                    drive_left.stop()
                    # tell the code that the right motor has been stopped
                    right_to_be_stopped = False
                else:
                    # reset the toggle so that the deadband code knows to stop the right motor next
                    # time the input is in the deadband range
                    right_to_be_stopped = True

        # only tell the left drive motor to spin if the values are not in the deadband range
        if left_to_be_stopped:
            drive_left.set_velocity(drivetrain_left_speed, PERCENT)
            drive_left.spin(FORWARD)
        # only tell the right drive motor to spin if the values are not in the deadband range
        if right_to_be_stopped:
            drive_right.set_velocity(drivetrain_right_speed, PERCENT)
            drive_right.spin(FORWARD)

        wait(20, MSEC)

rc_auto_loop = Thread(remote_control)


# Begin project code
# Create callback functions for each controller button event
# def controller_L1_Pressed():
#     arm_motor.spin(FORWARD)
#     while controller_1.buttonL1.pressing():
#         wait(5, MSEC)
#     arm_motor.stop()

# def controller_L2_Pressed():
#     arm_motor.spin(REVERSE)
#     while controller_1.buttonL2.pressing():
#         wait(5, MSEC)
#     arm_motor.stop()

# def controller_R1_Pressed():
#     claw_motor.spin(REVERSE)
#     while controller_1.buttonR1.pressing():
#         wait(5, MSEC)
#     claw_motor.stop()

# def controller_R2_Pressed():
#     claw_motor.spin(FORWARD)
#     while controller_1.buttonR2.pressing():
#         wait(5, MSEC)
#     claw_motor.stop()

# def startup_brain():
#     skills = [20 + 130 + 170 + 20, 170, 100, 50]
#     brain.screen.set_font(FontType.MONO30)
#     brain.screen.set_fill_color(Color.WHITE)
#     brain.screen.draw_rectangle(0, 0, 480, 272)
#     brain.screen.set_pen_color(Color.BLUE)
#     #brain.screen.draw_rectangle(10, 10, 460, 74, Color.BLACK)
#     brain.screen.set_cursor(1,9)
#     brain.screen.print("THE VEX VILLAINS")

#     # Replace with photo of field
#     # brain.screen.draw_image_from_file('field.bmp', 155, 46)

#     brain.screen.set_pen_color(Color.BLACK)

#     # Create Skills button
#     brain.screen.set_fill_color(Color.YELLOW)
#     brain.screen.draw_rectangle(skills[0], skills[1], skills[2], skills[3])
#     brain.screen.set_cursor(11,24)
#     brain.screen.print("Skills")

#     while brain.screen.pressing() == False:
#         wait(5, MSEC)


# def extendGrabber():
#     global isGrabbing
#     isGrabbing = not isGrabbing
#     print(isGrabbing)
#     grabber.set(isGrabbing)

def pneumatic_on():
    grabber.set(True)


def pneumatic_off():
    grabber.set(False)


controller_1.buttonUp.pressed(pneumatic_on)
controller_1.buttonDown.pressed(pneumatic_off)

pneumatic_off()
# startup_brain()

# Create Controller callback events - 15 msec delay to ensure events get registered
# controller_1.buttonL1.pressed(controller_L1_Pressed)
# controller_1.buttonL2.pressed(controller_L2_Pressed)
# controller_1.buttonR1.pressed(controller_R1_Pressed)
# controller_1.buttonR2.pressed(controller_R2_Pressed)
# controller_1.buttonA.pressed(extendGrabber)
# wait(15, MSEC)

# Configure Arm and Claw motor hold settings and velocity
# arm_motor.set_stopping(HOLD)
# claw_motor.set_stopping(HOLD)
# arm_motor.set_velocity(60, PERCENT)
# claw_motor.set_velocity(30, PERCENT)

# # Main Controller loop to set motors to controller axis postiions
# while True:
#     left_motor.set_velocity(controller_1.axis3.position(), PERCENT)
#     right_motor.set_velocity(controller_1.axis2.position(), PERCENT)
#     left_motor.spin(FORWARD)
#     right_motor.spin(FORWARD)
#     wait(5, MSEC)
