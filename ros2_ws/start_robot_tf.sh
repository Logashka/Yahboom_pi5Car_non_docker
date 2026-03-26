#!/bin/bash

# ROS 2
source /opt/ros/jazzy/setup.bash
source /home/pi/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=40

# Запуск bringup
ros2 launch my_two_wheel_robot two_wheel_robot.launch.py
