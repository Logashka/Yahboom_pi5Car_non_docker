import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    package_path = get_package_share_directory('yahboom_nav')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    namespece = LaunchConfiguration('namespace', default='')
    map_yaml_path = LaunchConfiguration(
        'maps', default=os.path.join('/home/pi/ros2_ws/src/yahboom_nav', 'maps', 'office_map.yaml')) 
    nav2_param_path = LaunchConfiguration('params_file', default=os.path.join(
        package_path, 'params', 'nav_param.yaml'))

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value=use_sim_time,
                              description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument('namespece', default_value=namespece,
                              description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument('maps', default_value=map_yaml_path,
                              description='Full path to map file to load'),
        DeclareLaunchArgument('params_file', default_value=nav2_param_path,
                              description='Full path to param file to load'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [nav2_bringup_dir, '/launch', '/bringup_launch.py']),
            launch_arguments={
                'map': map_yaml_path,
                'use_sim_time': use_sim_time,
                'namespece': namespece,
                'params_file': nav2_param_path}.items(),
        ),
        Node(
            package='yahboom_nav',
            executable='stop_car'
        )
    ])
