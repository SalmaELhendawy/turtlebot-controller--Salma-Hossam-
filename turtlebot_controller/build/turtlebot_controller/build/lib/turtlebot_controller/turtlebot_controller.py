import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty

# رسالة توضيحية للمستخدم في الترمينال لمعرفة أزرار التحكم
msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d

q : stop and exit
"""

# دالة مخصصة لقرأة حركة زر الكيبورد فوراً من الـ Terminal دون الحاجة لضغط Enter
def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class TurtlebotController(Node):
    def __init__(self):
        # تعريف اسم النود الخاصة بالتحكم
        super().__init__('turtlebot_controller')
        # إنشاء الـ Publisher على تووبك /cmd_vel بنوع رسالة Twist وبـ Queue size يساوي 10
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("Turtlebot Controller Node has been started.")

    def send_cmd(self, linear_x, angular_z):
        # بناء كائن الرسالة من نوع Twist وتعبئة قيم السرعة الخطية والزاوية
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        # نشر الرسالة فوراً على التووبك ليتحرك الروبوت
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    
    # حفظ إعدادات الترمينال الحالية للقراءة الحية والأوتوماتيكية للأزرار
    settings = termios.tcgetattr(sys.stdin)
    
    node = TurtlebotController()
    print(msg)
    
    try:
        while True:
            # استقبال الزر المضغوط من الكيبورد
            key = get_key(settings)
            
            linear_x = 0.0
            angular_z = 0.0
            
            # شروط تحديد قيم واتجاه الحركة بناء على الزر المختار
            if key == 'w':
                linear_x = 0.5   # حركة للأمام
                print("Command: Moving Forward")
            elif key == 's':
                linear_x = -0.5  # حركة للخلف
                print("Command: Moving Backward")
            elif key == 'a':
                angular_z = 1.0  # دوران لليسار
                print("Command: Turning Left")
            elif key == 'd':
                angular_z = -1.0 # دوران لليمين
                print("Command: Turning Right")
            elif key == 'q':
                # إيقاف الروبوت تماماً والخروج من اللوب عند ضغط زر Q
                node.send_cmd(0.0, 0.0)
                print("Command: Stopping robot and exiting...")
                break
            else:
                # أي زر عشوائي آخر يقوم بإيقاف الروبوت فوراً كإجراء أمان
                linear_x = 0.0
                angular_z = 0.0
            
            # إرسال السرعات المحدثة إلى التووبك
            node.send_cmd(linear_x, angular_z)
            
    except Exception as e:
        print(e)
    finally:
        # تأكيد إيقاف الروبوت تماماً وتدمير النود عند الإغلاق المفاجئ
        node.send_cmd(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

