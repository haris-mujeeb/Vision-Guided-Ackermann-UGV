from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
  use_sim_time_arg = DeclareLaunchArgument(
    "use_sim_time",
    default_value="True"
  )

  use_sim_time = LaunchConfiguration("use_sim_time")

  joint_state_broadcaster_spawner = Node(
    package="controller_manager",
    executable="spawner",
    arguments=[
      "joint_state_broadcaster",
      "--controller-manager",
      "/controller_manager",
    ],
    parameters=[{"use_sim_time": use_sim_time}]
  )

  ugv_controller_spawner = Node(
    package="controller_manager",
    executable="spawner",
    arguments=[
      "ugv_controller",
      "--controller-manager",
      "/controller_manager",
    ],
    parameters=[{"use_sim_time": use_sim_time}]
  )


  return LaunchDescription(
    [
      use_sim_time_arg,
      joint_state_broadcaster_spawner,
      ugv_controller_spawner
    ]
  )