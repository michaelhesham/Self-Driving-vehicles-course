from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
	obj_launch=LaunchDescription()
	
	node1=Node(
		package='test_pkg',
		executable='publisher'		
	)
	
	obj_launch.add_action(node1)	
	
	return obj_launch
