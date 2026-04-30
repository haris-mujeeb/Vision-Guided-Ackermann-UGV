import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory



def generate_launch_description():
  use_sim_time = LaunchConfiguration("use_sim_time")
  world_name = LaunchConfiguration("world_name")

  declare_use_sim_time_arg = DeclareLaunchArgument(
      'use_sim_time',
      default_value='true',
      description='Use simulation (Gazebo) clock if true'
    )
  
  declare_world_name_arg = DeclareLaunchArgument(
      'world_name',
      default_value='empty',
      description='World name'
    )
  
  gazebo = IncludeLaunchDescription(
    os.path.join(
      get_package_share_directory("ugv_description"),
      "launch",
      "sim.launch.py"
    ),
    launch_arguments={
      "use_sim_time": use_sim_time,
      "world_name": world_name,
    }.items()
  )

  control = IncludeLaunchDescription(
    os.path.join(
      get_package_share_directory("ugv_control"),
      "launch",
      "control.launch.py"
    ),
    launch_arguments={
      "use_sim_time": use_sim_time
    }.items()
  )
  
  joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("ugv_control"),
            "launch",
            "joystick_teleop.launch.py"
        ),
        launch_arguments={
            "use_sim_time": use_sim_time
        }.items()
    )

  return LaunchDescription([
    declare_use_sim_time_arg,
    declare_world_name_arg,
    gazebo,
    control,
    joystick,
  ])

