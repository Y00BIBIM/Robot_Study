#!/usr/bin/env python3

import rospy

def main():
    rospy.init_node('basic_robot_node')

    rospy.loginfo("Basic robot node started.")

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        rospy.loginfo("Robot node is running...")
        rate.sleep()

if __name__ == '__main__':
    main()
