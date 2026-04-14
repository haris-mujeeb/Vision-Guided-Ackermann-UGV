# ugv_vision

## General Idea
Processes and publishes the live stream from the actual robot's physical camera. This package is responsible for interfacing with the hardware camera and providing video data to the network.

## TODOs
- [ ] Setup `v4l2_camera` or a custom OpenCV node for the real camera.
- [ ] Configure `image_transport` (e.g., compressed format) for efficient streaming.
- [ ] Ensure proper TF frame IDs for the camera optical frame.
