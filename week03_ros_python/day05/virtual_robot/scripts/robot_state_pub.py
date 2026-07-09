#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def main():
    rospy.init_node('robot_state_node')

    pub = rospy.Publisher('/robot/state', String, queue_size=10)

    rate = rospy.Rate(1)

    x = 0.0
    y = 0.0
    speed = 0.0
    battery = 100.0

    while not rospy.is_shutdown():
        state_msg = f"x={x}, y={y}, speed={speed}, battery={battery}"

        pub.publish(state_msg)
        rospy.loginfo("Published robot state: %s", state_msg)

        battery -= 0.1

        if battery < 0:
            battery = 0

        rate.sleep()

if __name__ == '__main__':
    main()

