import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtlebotMonitor(Node):
    def __init__(self):
        # Initialize the subscriber node with the name 'turtlebot_monitor'
        super().__init__('turtlebot_monitor')
        
        # Create a subscriber to listen to the '/cmd_vel' topic
        # Message type: Twist, Callback function: listener_callback, Queue size: 10
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.listener_callback,
            10)
        self.get_logger().info("Turtlebot Monitor Node has been started and is listening...")

    def listener_callback(self, msg):
        # Extract linear velocity (forward/backward) and angular velocity (turning) from the incoming message
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # Print the received velocity values in a readable dashboard format
        print(f"[MONITOR] Robot State -> Linear X: {linear_x:.2f} | Angular Z: {angular_z:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = TurtlebotMonitor()
    try:
        # Keep the node running to continuously listen for incoming messages
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Handle manual shutdown (Ctrl+C) smoothly without crashes
        pass
    finally:
        # Destroy the node and shutdown ROS 2 safely on exit
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

