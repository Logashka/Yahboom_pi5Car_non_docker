# YB MicroROS-Pi5 Robot Car without docker

1) Use systemd-services to create autostart to microros-agent. If you don't create it, your stm32 board and RPi5 microcomputer will not be able to exchange messages
2) Use launch files from my_bringup to start base nodes, like EKF odometry and imu filter

# On the RPi5
Will start building the map

  ```ros2 launch slam_toolbox online_sync_launch.py ​​slam_params_file:=/home/pi/ros2_ws/slam_param.yaml use_sim_time:=false```

Save map

  ```ros2 run nav2_map_server map_saver_cli -f /home/pi/ros2_ws/maps/office_map ```
  
  ```ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph \ "{filename: '/home/pi/ros2_ws/maps/office_map'}"```

Localization
  
  ```ros2 launch slam_toolbox localization_launch.py ​​slam_params_file:=/home/pi/param/slam_loc.yaml``` 

Joystick control

  ```ros2 launch yahboomcar_ctrl yahboomcar_joy_launch.py```

Launch navigation

  ```ros2 launch yahboom_nav navigation_dwb_launch.py```

# On the PC:
  ```source ~/ros2_jazzy/install/local_setup.bash```
  
  ```source /opt/ros/jazzy/setup.bash```
  
  ```source ~/ros2_ws/install/setup.bash```

Visualization -
  ```rviz2 rviz2```

Control from keyboard-
  ```ros2 run teleop_twist_keyboard teleop_twist_keyboard```

View tree -
  ```ros2 run tf2_tools view_frames```


# If you want to check original src

```https://github.com/Logashka/Yahboom_pi5Car_src```
