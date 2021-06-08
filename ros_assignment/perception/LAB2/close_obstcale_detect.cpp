#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/point_cloud2.hpp"
#include "carkyo_msgs/msg/camera_emergency.hpp"

//#include <pcl_conversions/pcl_conversions.h>


 
using namespace std;


class PointcloudFilter : public rclcpp::Node
{
  public:
 
         
     PointcloudFilter()
    : Node("close_obstcale_detect")
    {          
      RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "create sub");
      subscriber_ = this->create_subscription<sensor_msgs::msg::PointCloud2>("intel/cropped", 5, std::bind(&PointcloudFilter::subscribe_message, this, std::placeholders::_1));

      publisher_emergency = this->create_publisher<carkyo_msgs::msg::CameraEmergency>("CameraEmergency", 10);

   } 

  private:

    void subscribe_message(const sensor_msgs::msg::PointCloud2::SharedPtr message) const
    {
    
    
        carkyo_msgs::msg::CameraEmergency cameraEmergency ;
        if(message->data.size() > 50)  	
		cameraEmergency.close_obstacle_detected = true;
        else
		cameraEmergency.close_obstacle_detected = false;
        
        
        publisher_emergency->publish(cameraEmergency);
        
       
    }
    rclcpp::Node::SharedPtr nh_;
   
    rclcpp::Publisher<carkyo_msgs::msg::CameraEmergency>::SharedPtr publisher_emergency;
        
    rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr subscriber_;
};

int main(int argc, char * argv[])
{
  RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Ready");
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PointcloudFilter>());
  rclcpp::shutdown();
  return 0;
}
