from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_path = get_package_share_path('my_two_wheel_robot')
    default_model_path = pkg_path / 'urdf' / 'MicroROS.urdf'

    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=str(default_model_path),
        description='Absolute path to robot urdf file'
    )

    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        output='screen'
    )

    tf_base_footprint_to_base_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0.05', '0.0', '0.0', '0.0', 'base_footprint', 'base_link'],
        output='screen'
    )

    return LaunchDescription([
        model_arg,
        joint_state_publisher_node,
        robot_state_publisher_node,
        tf_base_footprint_to_base_link
    ])
