# ugv_control

## General Idea
Motor control configurations, `ros2_control` parameters, and teleoperation routing. This package manages how commands (like `cmd_vel`) are translated into wheel velocities and steering angles.

## TODOs
- [ ] Configure `ackermann_steering_controller` in a YAML file.
- [ ] Configure `joint_state_broadcaster`.
- [ ] Set up a teleop node (keyboard or joystick) to publish `cmd_vel`.
- [ ] Write a launch file to load the controllers.
