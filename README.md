# vehicle-counter
Vehicle Counter Project on Videos using cv2
Absolute difference between frames is used as a technique.

# Input
traffic.avi video is need to run project.
You can download it.  
Frames are taken from this video.  

![alt text](https://github.com/mfsonmez/vehicle-counter/blob/0351822f46d1da04c56c2d9898b1da119e641ec1/Frames/img23.jpg)

Example input frame

# Running Steps
Project gets frames from traffic.avi video.
![alt text](https://github.com/mfsonmez/vehicle-counter/blob/0351822f46d1da04c56c2d9898b1da119e641ec1/AppliedMethods.PNG)

Absolute difference is applied between simultaneous frames.  
After absolute difference, otsu treshold, morphological operations and medianBlur are applied.  
At the end of these tasks, cv2 finds contours and found contours are marked.  

# Output
After image processing tasks, project creates video from processed images.

![alt text](https://github.com/mfsonmez/vehicle-counter/blob/0351822f46d1da04c56c2d9898b1da119e641ec1/Frames/img23_marked.jpg)

Example output frame
