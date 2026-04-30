import os
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

  ugv_control_pkg = get_package_share_directory("ugv_control")

  use_python_arg = DeclareLaunchArgument(
    "use_python",
    default_value="True",
  )

  use_sim_time_arg = DeclareLaunchArgument(
    "use_sim_time",
    default_value="true"
  )
  
  use_python = LaunchConfiguration("use_python")
  use_sim_time = LaunchConfiguration("use_sim_time")


  joy_node = Node(
    package="joy",
    executable="joy_node",
    name="joystick",
    parameters=[os.path.join(ugv_control_pkg, "config", "joy_config.yaml"), {'use_sim_time': use_sim_time}],
    remappings=[('/joy', '/joy_raw')]
  )

  joy_teleop = Node(
    package="joy_teleop",
    executable="joy_teleop",
    parameters=[os.path.join(ugv_control_pkg, "config", "joy_teleop.yaml"), {'use_sim_time': use_sim_time}]
  )

  twist_mux_launch = IncludeLaunchDescription(
    os.path.join(
      get_package_share_directory("twist_mux"),
      "launch",
      "twist_mux_launch.py"
    ),
    launch_arguments={
      "cmd_vel_out": "ugv_control/cmd_vel_unstamped",
      "config_locks": os.path.join(ugv_control_pkg, "config", "twist_mux_locks.yaml"),
      "config_topics": os.path.join(ugv_control_pkg, "config", "twist_mux_topics.yaml"),
      "config_joy": os.path.join(ugv_control_pkg, "config", "twist_mux_joy.yaml"),
      "use_sim_time": use_sim_time,
    }.items(),
  )

  twist_relay_node_py = Node(
    package="ugv_control",
    executable="twist_relay.py",
    name="twist_relay", 
    condition=IfCondition(use_python),
    parameters=[{'use_sim_time': use_sim_time}]
  )

  twist_relay_node = Node(
    package="ugv_control",
    executable="twist_relay",
    name="twist_relay", 
    condition=UnlessCondition(use_python),
    parameters=[{'use_sim_time': use_sim_time}]
  )

  joy_normalizer_node = Node(
    package="ugv_control",
    executable="joy_normalizer.py",
    name="joy_normalizer",
    parameters=[{'use_sim_time': use_sim_time}]
  )
  
  return LaunchDescription([
    use_python_arg,
    use_sim_time_arg,
    joy_teleop,
    joy_node,
    joy_normalizer_node,
    twist_mux_launch,
    twist_relay_node_py,
    twist_relay_node,
  ])