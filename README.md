# Obstacle Avoidance Robot

A ROS 2-based autonomous mobile robot designed to detect and avoid obstacles using sensor data and navigation logic.

The robot continuously monitors its surroundings and changes its motion when an obstacle is detected, allowing it to move safely through an environment.

## Features

- Autonomous obstacle detection
- Real-time obstacle avoidance
- Sensor-based environment perception
- Differential-drive robot simulation
- ROS 2 node-based control
- Gazebo simulation support
- RViz2 visualization

## Technologies Used

- ROS 2
- Python
- Gazebo
- RViz2
- LiDAR / Distance Sensors
- Differential Drive

## System Requirements

| Component | Requirement |
|---|---|
| Operating System | Ubuntu 24.04 |
| ROS 2 | Jazzy |
| Python | Python 3 |
| Gazebo | Gazebo Sim |

## Project Structure

```text
Obstacle-Avoidance-Robot/
│
└── src/
    └── obstacle_avoidance_bot/
        ├── launch/
        ├── config/
        ├── urdf/
        ├── worlds/
        ├── scripts/
        ├── resource/
        ├── test/
        ├── package.xml
        ├── setup.py
        └── setup.cfg
