import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory('my_bringup')
    # imu_filter_config = os.path.join(pkg_share, 'param', 'imu_filter_param.yaml')

    return LaunchDescription(
        [
            Node(
                package='imu_complementary_filter',
                executable='complementary_filter_node',
                name='complementary_filter_gain_node',
                output='screen',
                remappings=[('/imu/data_raw','/imu')],
                parameters=[
                    {'do_bias_estimation': True},
                    {'do_adaptive_gain': True},
                    {'use_mag': False},
                    {'gain_acc': 0.01},
                    {'gain_mag': 0.01},
                ],
            )
        ]
    )
