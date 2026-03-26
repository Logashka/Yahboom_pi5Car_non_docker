import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')

        # --- параметры ---
        self.declare_parameter('device', '/dev/video0')
        self.declare_parameter('width', 320)
        self.declare_parameter('height', 240)
        self.declare_parameter('fps', 60)
        self.declare_parameter('pixel_format', 'MJPG')

        device = self.get_parameter('device').value
        width = self.get_parameter('width').value
        height = self.get_parameter('height').value
        fps = self.get_parameter('fps').value
        pixel_format = self.get_parameter('pixel_format').value

        # --- openCV capture ---
        self.cap = cv2.VideoCapture(device, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

        # MJPG формат
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*pixel_format))

        if not self.cap.isOpened():
            self.get_logger().error('Cannot open camera')
            raise RuntimeError('Camera error')

        self.pub = self.create_publisher(Image, 'image_raw', 10)
        self.bridge = CvBridge()

        timer_period = 1.0 / fps
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info(f"Camera started at {width}x{height} @ {fps}fps ({pixel_format})")
        self.declare_parameter('frame_id', 'camera_frame')
        self.frame_id = self.get_parameter('frame_id').value
    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning('Failed to read frame')
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_frame'

        self.pub.publish(msg)

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
