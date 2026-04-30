#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped

class TwistRelayNode(Node):
  def __init__(self):
    super().__init__("twist_relay")

    # Relay twist_mux output (Twist) to ugv_controller input (TwistStamped)
    self.control_sub = self.create_subscription(
      Twist,
      "ugv_control/cmd_vel_unstamped",
      self.controlTwistCallback,
      10
    )

    self.control_pub = self.create_publisher(
      TwistStamped,
      "/ugv_controller/reference",
      10
    )

    # Relay joystick teleop output (TwistStamped) to twist_mux input (Twist)
    self.joy_sub = self.create_subscription(
      TwistStamped,
      "/input_joy/cmd_vel_stamped",
      self.joyTwistCallback,
      10
    )

    self.joy_pub = self.create_publisher(
      Twist,
      "/input_joy/cmd_vel",
      10
    )

  def controlTwistCallback(self, msg : Twist):
    stamped_msg = TwistStamped()
    stamped_msg.header.stamp = self.get_clock().now().to_msg()
    stamped_msg.header.frame_id = "base_link"
    stamped_msg.twist = msg
    self.control_pub.publish(stamped_msg)

  def joyTwistCallback(self, msg : TwistStamped):
    self.joy_pub.publish(msg.twist)


def main(args=None):
  rclpy.init(args=args)
  node = TwistRelayNode()
  rclpy.spin(node)
  node.destroy_node()
  rclpy.shutdown()

if __name__ == "__main__":
  main()