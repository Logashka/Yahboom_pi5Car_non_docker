#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class DriveSquare(Node):
    def __init__(self):
        super().__init__('drive_square')

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(Odometry, '/odom_raw', self.odom_callback, 10)

        self.timer = self.create_timer(0.05, self.update)

        self.start_x = None
        self.start_y = None
        self.start_yaw = None

        # Этапы движения:
        # 0 — начало
        # 1 — едем прямо 1 м
        # 2 — поворот 90°
        # 3 — снова прямо 1 м
        self.state = 0  

        self.twist = Twist()

    def odom_callback(self, msg):
        # Позиция
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        # Ориентация → yaw
        q = msg.pose.pose.orientation
        yaw = math.atan2(
            2.0*(q.w*q.z + q.x*q.y),
            1.0 - 2.0*(q.y*q.y + q.z*q.z)
        )
        self.yaw = yaw

    def update(self):
        if not hasattr(self, 'x'):
            return  # ещё нет данных одометрии

        # Сохраняем стартовую точку
        if self.start_x is None:
            self.start_x = self.x
            self.start_y = self.y
            self.start_yaw = self.yaw
            self.get_logger().info("Стартовая позиция записана")
            return

        dx = self.x - self.start_x
        dy = self.y - self.start_y
        dist = math.sqrt(dx*dx + dy*dy)

        dyaw = self.yaw - self.start_yaw
        dyaw = math.atan2(math.sin(dyaw), math.cos(dyaw))

        # --- ЛОГИКА ДВИЖЕНИЯ ---

        # 1) Едем вперёд 1 метр
        if self.state == 1:
            if dist < 1.0:
                self.twist.linear.x = 0.15
                self.twist.angular.z = 0.0
            else:
                self.stop()
                self.state = 2
                self.start_yaw = self.yaw  # обновляем старт угла
                self.get_logger().info("Проехали 1 метр, начинаем поворот")

        # 2) Поворот налево на 90 градусов
        elif self.state == 2:
            if dyaw < math.radians(90):
                self.twist.angular.z = 0.6
                self.twist.linear.x = 0.0
            else:
                self.stop()
                self.state = 3
                self.start_x = self.x
                self.start_y = self.y
                self.get_logger().info("Поворот 90° завершён, едем вперёд")

        # 3) Едем вперёд ещё 1 метр
        elif self.state == 3:
            if dist < 1.0:
                self.twist.linear.x = 0.15
            else:
                self.stop()
                self.state = 4
                self.get_logger().info("Маршрут завершён!")

        else:
            # Переход в state=1 после старта
            self.state = 1

        self.cmd_pub.publish(self.twist)

    def stop(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.cmd_pub.publish(self.twist)


def main(args=None):
    rclpy.init(args=args)
    node = DriveSquare()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
