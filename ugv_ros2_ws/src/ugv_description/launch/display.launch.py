import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
  ugv_description_dir = get_package_share_directory("ugv_description")
  default_model_path = os.path.join(ugv_description_dir, "urdf", "neor_mini.urdf")

  model_arg = DeclareLaunchArgument(
    name="model",
    default_value=default_model_path,
    description='Absolute path to robot urdf file'
  )

  # robot_description = ParameterValue(
  #     Command(['xacro ', LaunchConfiguration('model')]), 
  #     value_type=str
  #   )

  with open(default_model_path, 'r') as file:
    robot_description = file.read()

  robot_state_publisher_node = Node(
    package="robot_state_publisher",
    executable="robot_state_publisher",
    name='robot_state_publisher',
    output='screen',
    parameters=[{"robot_description": robot_description}]  
  )

  joint_state_publisher_gui_node = Node(
    package="joint_state_publisher_gui",
    executable="joint_state_publisher_gui",
    name="joint_state_publisher_gui",
    parameters=[{'robot_description': robot_description}]
  )

  rviz_node = Node(
    package='rviz2',
    executable='rviz2',
    name="rviz2",
    output='screen',
    arguments=['-d', os.path.join(ugv_description_dir, 'rviz/display.rviz')]
  )

  return LaunchDescription(
    [
      model_arg,
      robot_state_publisher_node,
      joint_state_publisher_gui_node,
      rviz_node,
    ]
  )