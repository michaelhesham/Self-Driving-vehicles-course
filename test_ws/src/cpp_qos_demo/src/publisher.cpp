#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"


/* This example creates a subclass of Node and uses std::bind() to register a
 * member function as a callback from the timer. */

class Publisher : public rclcpp::Node
{
public:
  Publisher()
  : Node("Node1")
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("str_topic", 10);
    timer_ = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&Publisher::timer_callback, this));
  }

private:
  void timer_callback()
  {
    std_msgs::msg::String message = std_msgs::msg::String();
    message.data = "Message: " + std::to_string(count_++);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    publisher_->publish(message);
  }
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  int count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Publisher>());
  rclcpp::shutdown();
  return 0;
}
