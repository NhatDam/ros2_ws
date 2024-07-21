import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():

  #this name has to match the robot name in the Xacro file
  robotXacroName= "AGV"
  
  # Set the path to the URDF file
  default_urdf_model_path = os.path.join(get_package_share_directory('robot_pkg'),'urdf/Model.urdf.xacro')

  # robotDescription = Command(['xacro ', default_urdf_model_path])
  robotDescription = xacro.process_file(default_urdf_model_path)
  xml = robotDescription.toxml()
 
  #this is the absolute path to the world model
  pathWorldFile = os.path.join(get_package_share_directory('robot_pkg'),'worlds/hello.world')

  # Load the URDF into a parameter
  # urdf = open(default_urdf_model_path).read()

  #this is the launch file from the gazebo_ros package
  gazebo_rosPackageLaunch = PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('gazebo_ros'),'launch'),'/gazebo.launch.py'])

  #this is the launch description
  gazeboLaunch=IncludeLaunchDescription(gazebo_rosPackageLaunch,launch_arguments={'world': pathWorldFile}.items())

  # Specify the actions
  #Here, we create a gazebo_ros Node
  spawnModeNode = Node(
    package='gazebo_ros', 
    executable='spawn_entity.py',
    name ='spawn_entity',
    arguments=['-entity', robotXacroName, '-topic', 'robot_description'],
    output='screen')
  

  # Publish Robot Desciption in String form in the topic /robot_description
  # publish_robot_description = Node(
  #       package='robot_pkg',
  #       executable='robot_description_publisher.py',
  #       name='robot_description_publisher',
  #       output='screen',
  #       arguments=['-xml_string', xml,
  #                  '-robot_description_topic', '/robot_description'
  #                  ]
  #   )

  # Subscribe to the joint states of the robot, and publish the 3D pose of each link.
  use_sim_time = LaunchConfiguration('use_sim_time', default='true')
  start_robot_state_publisher_cmd = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    name='robot_state_publisher',
    output='screen',
    parameters=[{'robot_description': xml,'use_sim_time': use_sim_time}],
    )
  
  
  # Create the launch description and populate
  ld = LaunchDescription()
 
  # Declare the launch options
  # Add gazeboLaunch
  # ld.add_action(publish_robot_description)
  ld.add_action(start_robot_state_publisher_cmd)
  ld.add_action(gazeboLaunch)
  # Add any actions
  ld.add_action(spawnModeNode)
  return ld
