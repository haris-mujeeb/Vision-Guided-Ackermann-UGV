import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression, PathJoinSubstitution, Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
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

  world_name_arg = DeclareLaunchArgument(name="world_name", default_value="empty")

  world_path = PathJoinSubstitution([
    ugv_description_dir, 
    "worlds",
    PythonExpression(expression=[
        "'", 
        LaunchConfiguration("world_name"), 
        "'", 
        " + '.world'"
      ]) 
  ])



  # Get the parent directory of ugv_description to allow Gazebo to find the package
  pkg_project_description = get_package_share_directory('ugv_description')
  parent_dir = os.path.dirname(pkg_project_description)

  # Create a symlink in a space-free path (/tmp) to avoid ROS 2 parameter parsing issues with spaces
  controller_params_src = os.path.join(get_package_share_directory('ugv_control'), 'config', 'ugv_controller.yaml')
  tmp_params_path = '/tmp/ugv_controller.yaml'
  if os.path.exists(tmp_params_path):
      os.remove(tmp_params_path)
  os.symlink(controller_params_src, tmp_params_path)

  # Use xacro to process the file and inject the tmp path
  robot_description_content = Command([
    'xacro "', LaunchConfiguration('model'), '" ',
    'controller_params:=', tmp_params_path
  ])
  robot_description = ParameterValue(robot_description_content, value_type=str)

  robot_state_publisher_node = Node(
    package="robot_state_publisher",
    executable="robot_state_publisher",
    name='robot_state_publisher',
    output='screen',
    parameters=[{"robot_description": robot_description, "use_sim_time": True}]  
  )

  rviz_node = Node(
    package='rviz2',
    executable='rviz2',
    name="rviz2",
    output='screen',
    arguments=['-d', os.path.join(ugv_description_dir, 'rviz/display.rviz')],
    parameters=[{"use_sim_time": True}]
  )

  # Set GZ_SIM_RESOURCE_PATH so Gazebo can find models and meshes
  gazebo_resource_path = SetEnvironmentVariable(
    'GZ_SIM_RESOURCE_PATH', 
    parent_dir
  )

  gazebo_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
    ),
    launch_arguments={
      "gz_args": PythonExpression(["'\"' + '", world_path, "' + '\" -v 4 -r'"])
    }.items()
  )


  gazebo_spawn_robot = Node(
    package='ros_gz_sim',
    executable='create',
    output='screen',
    arguments=[
      '-topic', 'robot_description',
      '-name', 'ugv',
      '-x', '0.0',
      '-y', '0.0',
      '-z', '0.2'
    ]
  )


  gazebo_ros2_bridge = Node(
     package="ros_gz_bridge",
     executable="parameter_bridge",
     arguments=[
      '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
     ],
     output='screen'
  )


  return LaunchDescription(
    [
      model_arg,
      robot_state_publisher_node,
      rviz_node,
      world_name_arg,
      gazebo_resource_path,
      gazebo_launch,
      gazebo_spawn_robot,
      gazebo_ros2_bridge,
    ]
  )