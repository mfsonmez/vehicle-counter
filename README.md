# vehicle-counter
Vehicle Counter Project on Videos using cv2
Absolute difference between frames is used as a technique.

# Input
traffic.avi video is need to run project.
You can download it.

# Running Steps
Project get frames from traffic.avi video.
Absolute difference is applied between simultaneous frames.
After absolute difference, otsu treshold, morphological operations and medianBlur are applied.
At the end of these tasks, cv2 finds contours and found contours are marked.

# Output
After image processing tasks, project creates video from processed images.
