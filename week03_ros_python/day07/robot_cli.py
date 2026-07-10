#!/usr/bin/env python3

import rospy
from virtual_robot.msg import RobotCommand

def print_menu():
    print("")
    print("===== Virtual Robot CLI =====")
    print("1. forward")
    print("2. backward")
    print("3. turn_left")
    print("4. turn_right")
    print("5. stop")
    print("q. quit")
    print("=============================")

def convert_input_to_command(user_input):
    if user_input == "1":
        return "forward"
    elif user_input == "2":
        return "backward"
    elif user_input == "3":
        return "turn_left"
    elif user_input == "4":
        return "turn_right"
    elif user_input == "5":
        return "stop"
    else:
        return None

def main():
    rospy.init_node('robot_cli_node')

    pub = rospy.Publisher('/robot/command', RobotCommand, queue_size=10)

    rospy.sleep(1.0)

    rospy.loginfo("Robot CLI node started.")

    while not rospy.is_shutdown():
        print_menu()
        user_input = input("Select command: ").strip().lower()

        if user_input == "q":
            rospy.loginfo("Robot CLI node finished.")
            break

        command = convert_input_to_command(user_input)

        if command is None:
            print("Invalid input. Please select again.")
            continue

        target_speed = 0.0

        if command in ["forward", "backward"]:
            try:
                target_speed = float(input("Input target speed: "))
            except ValueError:
                print("Invalid speed. Speed will be set to 0.0.")
                target_speed = 0.0

        msg = RobotCommand()
        msg.command = command
        msg.target_speed = target_speed

        pub.publish(msg)

        rospy.loginfo("Published command: %s, target_speed: %.2f", command, target_speed)

if __name__ == '__main__':
    main()
