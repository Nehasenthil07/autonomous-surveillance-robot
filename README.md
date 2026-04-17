# Autonomous Surveillance Robot

## Overview
AI-based surveillance system using YOLO and ROS2.

## Output
(Add screenshot here)

## Features
- Human detection using YOLOv8
- Alert system (sound + print)
- Image capture of intruder
- Robot movement using /cmd_vel

## Architecture
Camera → OpenCV → YOLO → Decision → Action

## How to Run
python3 yolo_detect.py
