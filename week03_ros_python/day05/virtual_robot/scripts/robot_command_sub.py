#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

current_command = "stop"

def command_callback(msg):
    global current_command

    command = msg.data.strip().lower()

    if command == "forward":
        current_command = command
        rospy.loginfo("Command received: FORWARD")
        rospy.loginfo("Robot will move forward.")

    elif command == "backward":
        current_command = command
        rospy.loginfo("Command received: BACKWARD")
        rospy.loginfo("Robot will move backward.")

    elif command == "turn_left":
        current_command = command
        rospy.loginfo("Command received: TURN LEFT")
        rospy.loginfo("Robot will rotate left.")

    elif command == "turn_right":
        current_command = command
        rospy.loginfo("Command received: TURN RIGHT")
        rospy.loginfo("Robot will rotate right.")

    elif command == "stop":
        current_command = command
        rospy.loginfo("Command received: STOP")
        rospy.loginfo("Robot will stop.")

    else:
        rospy.logwarn("Unknown command: %s", command)
        rospy.logwarn("Available commands: forward, backward, turn_left, turn_right, stop")

def main():
    rospy.init_node('robot_command_node')

    rospy.Subscriber('/robot/command', String, command_callback)

    rospy.loginfo("Robot command subscriber node started.")
    rospy.loginfo("Waiting for commands on /robot/command...")

    rospy.spin()

if __name__ == '__main__':
    main()
