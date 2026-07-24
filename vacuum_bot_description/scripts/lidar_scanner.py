#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32MultiArray

class LidarScanner(Node):
    def __init__(self):
        super().__init__('lidar_scanner')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.publisher_ = self.create_publisher(Float32MultiArray, '/processed_scan', 10)
        self.get_logger().info('Lidar Scanner Node Started!')

    def scan_callback(self, msg):
        ranges = msg.ranges
        num_ranges = len(ranges)
        if num_ranges == 0:
            return

        front_idx = num_ranges // 2
        left_idx = (num_ranges * 3) // 4
        right_idx = num_ranges // 4

        def get_valid_dist(idx_range):
            valid = [r for r in idx_range if not float('inf') == r and r > 0.1]
            return min(valid) if valid else 10.0

        front_dist = get_valid_dist(ranges[front_idx - 20 : front_idx + 20])
        left_dist = get_valid_dist(ranges[left_idx - 20 : left_idx + 20])
        right_dist = get_valid_dist(ranges[right_idx - 20 : right_idx + 20])

        out_msg = Float32MultiArray()
        out_msg.data = [front_dist, left_dist, right_dist]
        self.publisher_.publish(out_msg)

        self.get_logger().info(f'Distances -> Front: {front_dist:.2f}m | Left: {left_dist:.2f}m | Right: {right_dist:.2f}m')

def main(args=None):
    rclpy.init(args=args)
    node = LidarScanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()