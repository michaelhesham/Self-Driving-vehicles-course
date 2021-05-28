#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/int32.hpp"

class Subscriber : public rclcpp::Node
{
public:
  Subscriber()
  : Node("Node2")
  {
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "str_topic", 10, std::bind(&Subscriber::topic_callback, this, std::placeholders::_1));
    int_publisher_ = this->create_publisher<std_msgs::msg::Int32>("int_fb", 10);
  }

private:
  void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
  {
    RCLCPP_WARN(this->get_logger(), "I heard: '%s'", msg->data.c_str());
    std::string s = msg->data;
    std::string delimiter = ":";
    std::string number = s.substr(s.find(delimiter)+1, -1);
    RCLCPP_INFO(this->get_logger(), "string %s after split '%s'", s.c_str(), number.c_str());
    std_msgs::msg::Int32 message =  std_msgs::msg::Int32();
    message.data = std::stoi(number);
    int_publisher_->publish(message);
  }
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
  rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr int_publisher_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Subscriber>());
  rclcpp::shutdown();
  return 0;
}
