#!/usr/bin/env python3

import rospy
import math

from virtual_robot.msg import RobotState
from virtual_robot.msg import RobotCommand

class VirtualRobot:
    def __init__(self):
        rospy.init_node('virtual_robot_node')

        self.robot_id = "robot_01"

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.speed = 0.0
        self.battery = 100.0
        self.status = "stopped"

        self.state_pub = rospy.Publisher('/robot/state', RobotState, queue_size=10)

        self.command_sub = rospy.Subscriber(
            '/robot/command',
            RobotCommand,
            self.command_callback
        )

        self.timer = rospy.Timer(
            rospy.Duration(1.0),
            self.timer_callback
        )

        rospy.loginfo("Virtual robot node started.")

    def command_callback(self, msg):
        command = msg.command.strip().lower()
        target_speed = msg.target_speed

        rospy.loginfo("Command received: %s, target_speed: %.2f", command, target_speed)

        if command == "forward":
            self.speed = abs(target_speed)
            self.status = "moving_forward"

        elif command == "backward":
            self.speed = -abs(target_speed)
            self.status = "moving_backward"

        elif command == "turn_left":
            self.theta += 0.2
            self.speed = 0.0
            self.status = "turning_left"

        elif command == "turn_right":
            self.theta -= 0.2
            self.speed = 0.0
            self.status = "turning_right"

        elif command == "stop":
            self.speed = 0.0
            self.status = "stopped"

        else:
            rospy.logwarn("Unknown command: %s", command)
            self.status = "error_unknown_command"

    def timer_callback(self, event):
        self.update_robot_state()
        self.publish_robot_state()

    def update_robot_state(self):
        self.x += self.speed * math.cos(self.theta)
        self.y += self.speed * math.sin(self.theta)

        if self.speed != 0.0:
            self.battery -= 0.5
        else:
            self.battery -= 0.1

        if self.battery < 0.0:
            self.battery = 0.0
            self.speed = 0.0
            self.status = "battery_empty"

    def publish_robot_state(self):
        msg = RobotState()

        msg.robot_id = self.robot_id
        msg.x = self.x
        msg.y = self.y
        msg.theta = self.theta
        msg.speed = self.speed
        msg.battery = self.battery
        msg.status = self.status

        self.state_pub.publish(msg)

        rospy.loginfo(
            "State published: id=%s, x=%.2f, y=%.2f, theta=%.2f, speed=%.2f, battery=%.2f, status=%s",
            msg.robot_id,
            msg.x,
            msg.y,
            msg.theta,
            msg.speed,
            msg.battery,
            msg.status
        )

if __name__ == '__main__':
    robot = VirtualRobot()
    rospy.spin()
