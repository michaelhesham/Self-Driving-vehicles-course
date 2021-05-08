from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
	obj_launch=LaunchDescription()
	
	node1=Node(
		package='ros2_project',
		executable='spawn'		
	)
	
	node2=Node(
		package='ros2_project',
		executable='control'		
	)
	
	node3=Node(
		package='turtlesim',
		executable='turtlesim_node'		
	)
	
	obj_launch.add_action(node3)
	obj_launch.add_action(node1)
	obj_launch.add_action(node2)	
	
	return obj_launch
