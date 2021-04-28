#include <chrono>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/int32.hpp"
#include <bits/stdc++.h>
#include <boost/algorithm/string.hpp>

class Node2 : public rclcpp::Node
{
public:
    Node2():Node("Node2")
    {
        string_subscriber_ = this->create_subscription<std_msgs::msg::String>("str_topic",10, std::bind(&Node2::timer_cb, this, std::placeholders::_1));
        
        int32_publisher_ = this->create_publisher<std_msgs::msg::Int32>("int_fb",10);
        timer_ = this->create_wall_timer(std::chrono::milliseconds(1000), std::bind(&Node2::pub_timer, this));
    }
private:
    mutable int counter;
    void timer_cb(const std_msgs::msg::String::SharedPtr msg)const
    {
    	std::string str_msg ;
    	std::vector<std::string> result;
    	str_msg = msg->data.c_str();
    	boost::split(result, str_msg, boost::is_any_of(":"));
    	counter = std::stoi(result[1]);
    }
    
    void pub_timer()
    {
        std_msgs::msg::Int32 int32_msg = std_msgs::msg::Int32();
        int32_msg.data = counter;
        RCLCPP_INFO(this->get_logger(),std::to_string(int32_msg.data));
        int32_publisher_->publish(int32_msg);
    }
    
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr string_subscriber_;
    
    
    rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr int32_publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Node2>());
    rclcpp::shutdown();
    return 0;
}
