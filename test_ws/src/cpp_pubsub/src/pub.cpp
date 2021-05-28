#include "rclcpp/rclcpp.cpp"
#include "std_msgs/msg/string.hpp"

class Node1 : public rclcpp::Node{
    public:
        Node1():Node("string publisher"){

        }
    private:
        rclcpp:publisher<std_msgs::msg::Strings>::
};
