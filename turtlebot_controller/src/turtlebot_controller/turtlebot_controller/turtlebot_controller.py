import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty

# Instructions displayed to the user in the terminal
msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d

q : stop and exit
"""

# Function to capture keyboard strokes instantly without waiting for Enter
def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class TurtlebotController(Node):
    def __init__(self):
        # Initialize the publisher node with the name 'turtlebot_controller'
        super().__init__('turtlebot_controller')
        # Create a publisher on the '/cmd_vel' topic using the Twist message type
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("Turtlebot Controller Node has been started.")

    def send_cmd(self, linear_x, angular_z):
        # Construct the Twist message and populate linear and angular velocity fields
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        # Publish the command to the topic to move the robot
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    
    # Save current terminal settings to handle raw keyboard input smoothly
    settings = termios.tcgetattr(sys.stdin)
    
    node = TurtlebotController()
    print(msg)
    
    try:
        while True:
            # Capture the pressed key from the keyboard
            key = get_key(settings)
            
            linear_x = 0.0
            angular_z = 0.0
            
            # Conditions to map keys to corresponding movement velocities
            if key == 'w':
                linear_x = 0.5   # Move Forward
                print("Command: Moving Forward")
            elif key == 's':
                linear_x = -0.5  # Move Backward
                print("Command: Moving Backward")
            elif key == 'a':
                angular_z = 1.0  # Turn Left
                print("Command: Turning Left")
            elif key == 'd':
                angular_z = -1.0 # Turn Right
                print("Command: Turning Right")
            elif key == 'q':
                # Stop the robot completely and break the loop on 'q'
                node.send_cmd(0.0, 0.0)
                print("Command: Stopping robot and exiting...")
                break
            else:
                # Safety fallback: any other key stops the robot
                linear_x = 0.0
                angular_z = 0.0
            
            # Publish the updated velocities
            node.send_cmd(linear_x, angular_z)
            
    except Exception as e:
        print(e)
    finally:
        # Ensure the robot stops and resources are cleaned up on abrupt exit
        node.send_cmd(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()