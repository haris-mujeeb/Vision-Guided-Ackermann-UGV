# ugv_bringup

## General Idea
Centralized launch and configuration entry points for the entire system. This package simplifies starting different parts of the project with single commands.

## TODOs
- [ ] Write `sim.launch.py` (starts Gazebo, controllers, RViz, and simulated camera stream).
- [ ] Write `robot.launch.py` (starts hardware interface, real camera, and controllers).
- [ ] Write `teleop.launch.py` (starts remote control nodes on the base station).
