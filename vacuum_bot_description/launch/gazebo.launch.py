import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('vacuum_bot_description')
    world_path = os.path.join(pkg_dir, 'worlds', 'roomba_world.sdf')
    urdf_path = os.path.join(pkg_dir, 'urdf', 'robot.urdf.xacro')

    import xacro
    doc = xacro.parse(open(urdf_path))
    xacro.process_doc(doc)
    robot_description = {'robot_description': doc.toxml()}

    # 1. Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # 2. Gazebo Sim
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    # 3. Spawn Robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-string', doc.toxml(), '-name', 'vacuum_bot', '-x', '0.0', '-y', '0.0', '-z', '0.1'],
        output='screen'
    )

    # 4. ROS-GZ Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V'
        ],
        output='screen'
    )

    # 5. RQT Image View Window
    rqt_image_view = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        arguments=['/camera/image_raw'],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_robot,
        bridge,
        rqt_image_view
    ])