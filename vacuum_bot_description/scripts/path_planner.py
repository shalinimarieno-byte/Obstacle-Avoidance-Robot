#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')
        
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )
        
        self.get_logger().info('Lidar Obstacle Avoidance Path Planner Active!')

    def scan_callback(self, msg: LaserScan):
        cmd = Twist()
        
        if not msg.ranges:
            return

        # Split scan into front degrees (+/- 30 deg)
        front_ranges = msg.ranges[0:30] + msg.ranges[-30:]
        valid_front = [r for r in front_ranges if 0.15 < r < 10.0 and not float('inf') == r]
        
        min_front = min(valid_front) if valid_front else 10.0

        # Avoidance distance threshold: 0.8m
        if min_front < 0.8:
            self.get_logger().warn(f'Obstacle detected at {min_front:.2f}m! Turning Right...')
            cmd.linear.x = 0.0
            cmd.angular.z = -0.6
        else:
            self.get_logger().info(f'Path Clear ({min_front:.2f}m). Moving Forward.', throttle_duration_sec=1.0)
            cmd.linear.x = 0.25
            cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()