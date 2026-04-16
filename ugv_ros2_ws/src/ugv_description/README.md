# ugv_description

## General Idea
Contains the physical, collision, and visual properties of the 4-wheel Ackermann UGV. This package defines the URDF/Xacro models used by both the simulation (Gazebo) and the real robot (for state estimation and visualization).
Environment and launch files for Gazebo simulation. This package handles spawning the robot model into virtual worlds and setting up the simulation environment.

## TODOs
- [ ] Write base URDF/Xacro for the chassis.
- [ ] Add 4 wheels and configure Ackermann steering joints.
- [ ] Add camera sensor link and Gazebo plugin.
- [ ] Add IMU/Odometry plugins for Gazebo.
- [ ] Verify model in RViz.
- [ ] Create an empty Gazebo world.
- [ ] Create a test track world with obstacles.
- [ ] Write a launch file (`sim.launch.py`) to spawn the UGV in Gazebo.
