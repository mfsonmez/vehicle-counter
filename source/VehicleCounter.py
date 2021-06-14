import os
import re
import numpy as np
import cv2
import imutils 
from os.path import isfile, join

def GetFramesFromVideo(path):
    inputVideo = cv2.VideoCapture(path) 
       
    # Check if camera opened successfully 
    if (inputVideo.isOpened()== False):  
      print("Error opening video  file") 
    
    counter = 0
    
    # Read until video is completed 
    while(inputVideo.isOpened()): 
          
      # Capture frame-by-frame 
      ret, frame = inputVideo.read() 
      if ret == True: 
        cv2.imwrite('frames/img' + str(counter) + '.jpg', frame)
        counter = counter + 1
        # Press Q on keyboard to  exit 
        if cv2.waitKey(5) & 0xFF == ord('q'): 
          break
       
      # Break the loop 
      else:  
        break
       
    # When everything done, release  
    # the video capture object 
    inputVideo.release() 

def ShowVideo(path):
    selectedVideo = cv2.VideoCapture(path) 
   
    # Check if camera opened successfully 
    if (selectedVideo.isOpened()== False):  
      print("Error opening video  file") 
       
    # Read until video is completed 
    while(selectedVideo.isOpened()): 
          
      # Capture frame-by-frame 
      ret, frame = selectedVideo.read() 
      if ret == True: 
        height, width, layers = frame.shape
        new_h = height * 2
        new_w = width * 2
        resize = cv2.resize(frame, (new_w, new_h))
          # Display the resulting frame 
        cv2.imshow('Vehicle Detection on Traffic', resize)
       
        # Press Q on keyboard to  exit 
        if cv2.waitKey(100) & 0xFF == ord('q'): 
          break
       
      # Break the loop 
      else:  
        break
       
    # When everything done, release  
    # the video capture object 
    selectedVideo.release() 
    # Closes all the frames 
    cv2.destroyAllWindows() 

def CreateVideoFromFrames(FramePath, VideoOutPath):

    # specify frames per second
    fps = 5.0
    
    frame_array = []
    
    files = [f for f in os.listdir(FramePath) if isfile(join(FramePath, f))]
    
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    
    for i in range(len(files)):
        filename=pathIn + files[i]
        
        #read frames
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        
        #inserting the frames into an image array
        frame_array.append(img)
    
    out = cv2.VideoWriter(VideoOutPath,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    
    out.release()
    
try:
    os.mkdir('frames/')
    GetFramesFromVideo('traffic.avi')
except OSError:
    print ("Creation of the directory %s failed" % 'results/')

# kernel for image dilation
kernel = np.ones((4,4),np.uint8)

# font style
font = cv2.FONT_HERSHEY_SIMPLEX

# get file names of the frames
col_frames = os.listdir('frames/')

# sort file names
col_frames.sort(key=lambda f: int(re.sub('\D', '', f)))

#empty list to store the frames
col_images=[]

for i in col_frames:
    # read the frames
    img = cv2.imread('frames/'+i)
    # append the frames to the list
    col_images.append(img)

for i in range(len(col_images) -1):

    # convert the frames to grayscale
    grayA = cv2.cvtColor(col_images[i], cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(col_images[i+1] , cv2.COLOR_BGR2GRAY)
    diff_image = cv2.absdiff(grayB, grayA)
        
    #plt.imshow(diff_image, cmap = 'gray')
    #plt.show()

    otsu_threshold, image_result = cv2.threshold(diff_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    image_result = cv2.medianBlur(image_result,3)

    image_result = cv2.morphologyEx(image_result, cv2.MORPH_CLOSE, np.ones([8, 8]))  # gurultuden kurtul
    #image_result = cv2.morphologyEx(image_result, cv2.MORPH_OPEN, np.ones([5, 5]))  # gurultuden kurtul
    
    cnts = cv2.findContours(image_result.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cX, cY = 0, 0
        
    for c in cnts:
    	# compute the center of the contour
    	M = cv2.moments(c)
        
    	if M["m00"] != 0:
            cX = int(M["m10"] / (M["m00"]))
            cY = int(M["m01"] / (M["m00"]))

    	# draw the contour and center of the shape on the image
    	cv2.drawContours(col_images[i], [c], -1, (0, 0, 255), 1)
    	cv2.circle(col_images[i], (cX, cY), 1, (255, 0, 0), -1)
    	#cv2.putText(with_car_image, "center", (cX-5, cY-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (255, 255, 255), 2, cv2.LINE_AA)
    
    count, comp = cv2.connectedComponents(image_result)
    
    text = "Count: " + str(count - 1)
    cv2.putText(col_images[i], text, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (255, 255, 255), 2, cv2.LINE_AA)
    
    
    cv2.imwrite('results/img' + str(i) + '.jpg', col_images[i])
    
# specify video name
pathOut = 'VehicleDetection.mp4'
pathIn = "results/"

CreateVideoFromFrames(pathIn, pathOut)
ShowVideo(pathOut)

print("finished")