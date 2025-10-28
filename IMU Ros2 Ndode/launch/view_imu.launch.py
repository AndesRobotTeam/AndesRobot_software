from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    rviz_config_path = os.path.join(
        get_package_share_directory('hfi_b9_imu'),
        'hfi_b9_imu',
        'imu_view.rviz'  # si no existe, RViz se abre vacío
    )

    return LaunchDescription([
        # Nodo del IMU
        Node(
            package='hfi_b9_imu',
            executable='hfi_b9_imu_node',
            name='hfi_b9_imu',
            output='screen'
        ),

        # RViz con la vista (si existe la config)
        ExecuteProcess(
            cmd=['rviz2', '-d', rviz_config_path],
            output='screen'
        ),
    ])

