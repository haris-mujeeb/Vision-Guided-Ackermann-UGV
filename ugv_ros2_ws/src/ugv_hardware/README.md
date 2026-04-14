# ugv_hardware

## General Idea
The custom `ros2_control` hardware interface linking the ROS controllers to the physical motors and steering mechanisms of the real robot.

## TODOs
- [ ] Write a custom `SystemInterface` C++ plugin for `ros2_control`.
- [ ] Establish Serial/CAN communication with the motor controllers (e.g., Arduino/ESP32).
- [ ] Implement read/write loops for wheel velocities and steering angles.
