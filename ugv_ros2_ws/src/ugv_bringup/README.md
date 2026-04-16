# ugv_bringup

## General Idea
Centralized launch and configuration entry points for the entire system. This package simplifies starting different parts of the project with single commands.

## How to run 
```bash
colcon build && source ./install/setup.bash && ros2 launch ugv_bringup ugv.launch.py 
```


``` bash
ros2 topic pub /ugv_controller/reference geometry_msgs/msg/TwistStamped '{header: {stamp: "now", frame_id: "base_link"}, twist: {linear: {x: 1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}}' -r 10

```
## TODOs
- [x] Write `sim.launch.py` (starts Gazebo, controllers, and RViz).
- [ ] Fix Rviz not updating
- [ ] Add joystick control 
- [ ] Add simulated camera stream launch file 