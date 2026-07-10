#!/usr/bin/env python3

import rospy
import math

from virtual_robot.msg import RobotState
from virtual_robot.msg import RobotCommand


class VirtualRobot:
    def __init__(self):
        rospy.init_node('virtual_robot_node')

        # Robot state
        self.robot_id = "robot_01"
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.speed = 0.0
        self.battery = 100.0
        self.status = "stopped"

        # Settings
        self.max_speed = 5.0
        self.battery_move_usage = 0.5
        self.battery_idle_usage = 0.1

        # Publisher: robot state
        self.state_pub = rospy.Publisher(
            '/robot/state',
            RobotState,
            queue_size=10
        )

        # Subscriber: robot command
        self.command_sub = rospy.Subscriber(
            '/robot/command',
            RobotCommand,
            self.command_callback
        )

        # Timer: update and publish robot state every 1 second
        self.timer = rospy.Timer(
            rospy.Duration(1.0),
            self.timer_callback
        )

        rospy.loginfo("Virtual robot node started.")
        rospy.loginfo("Publishing robot state to /robot/state")
        rospy.loginfo("Subscribing robot command from /robot/command")

    def is_valid_command(self, command):
        valid_commands = [
            "forward",
            "backward",
            "turn_left",
            "turn_right",
            "stop"
        ]

        return command in valid_commands

    def validate_speed(self, target_speed):
        if target_speed < 0:
            rospy.logwarn(
                "Target speed is negative. It will be converted to positive value."
            )
            return abs(target_speed)

        if target_speed > self.max_speed:
            rospy.logwarn(
                "Target speed is too high. Max speed is limited to %.2f.",
                self.max_speed
            )
            return self.max_speed

        return target_speed

    def command_callback(self, msg):
        try:
            command = msg.command.strip().lower()
            target_speed = self.validate_speed(msg.target_speed)

            rospy.loginfo(
                "Command received: %s, target_speed: %.2f",
                command,
                target_speed
            )

            if not self.is_valid_command(command):
                rospy.logwarn("Unknown command received: %s", command)
                self.speed = 0.0
                self.status = "error_unknown_command"
                return

            if self.battery <= 0.0:
                rospy.logerr("Battery is empty. Robot cannot move.")
                self.speed = 0.0
                self.status = "battery_empty"
                return

            if command == "forward":
                self.speed = target_speed
                self.status = "moving_forward"
                rospy.loginfo("Robot is moving forward.")

            elif command == "backward":
                self.speed = -target_speed
                self.status = "moving_backward"
                rospy.loginfo("Robot is moving backward.")

            elif command == "turn_left":
                self.theta += 0.2
                self.speed = 0.0
                self.status = "turning_left"
                rospy.loginfo("Robot is turning left.")

            elif command == "turn_right":
                self.theta -= 0.2
                self.speed = 0.0
                self.status = "turning_right"
                rospy.loginfo("Robot is turning right.")

            elif command == "stop":
                self.speed = 0.0
                self.status = "stopped"
                rospy.loginfo("Robot stopped.")

        except Exception as e:
            rospy.logerr("Error while processing command: %s", str(e))
            self.speed = 0.0
            self.status = "error_exception"

    def timer_callback(self, event):
        try:
            self.update_robot_state()
            self.publish_robot_state()

        except Exception as e:
            rospy.logerr("Error in timer callback: %s", str(e))
            self.speed = 0.0
            self.status = "error_timer_exception"

    def update_robot_state(self):
        # Update position based on speed and direction
        self.x += self.speed * math.cos(self.theta)
        self.y += self.speed * math.sin(self.theta)

        # Decrease battery
        if self.speed != 0.0:
            self.battery -= self.battery_move_usage
        else:
            self.battery -= self.battery_idle_usage

        # Battery limit
        if self.battery <= 0.0:
            self.battery = 0.0
            self.speed = 0.0
            self.status = "battery_empty"
            rospy.logerr("Battery is empty. Robot stopped automatically.")

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
    try:
        robot = VirtualRobot()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("Virtual robot node interrupted.")

    except Exception as e:
        rospy.logerr("Unexpected error in virtual_robot_node: %s", str(e))
