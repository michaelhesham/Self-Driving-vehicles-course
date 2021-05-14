# ROS2 Project
## Description
Looks like a snake game but has all the ROS concepts to operate a robot with strating point to navigate getting goal position and path planning to achieve this goal with control algorithm on velocity although kill and spawn services are used

## Installation

in your_workspace/src:
```
git clone https://github.com/michaelhesham/Self-Driving-vehicles-course/tree/master/ros_assignment/project/ros2_project
```
in your_workspace:
```
colcon build --packages-select ros2_project
```
in new terminal:
```
ros2 launch ros2_project ros2_project.launch.py 
```
