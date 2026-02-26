import numpy as np
import cv2
from picamera2 import Picamera2
from libcamera import controls
import time

# Initialize Pi Camera
picam2 = Picamera2()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.start()
time.sleep(1)  # Give camera time to start up

# Define color range for line detection (adjust these values for your specific color)
lower_color = np.array([0, 0, 0])  # Lower HSV threshold
upper_color = np.array([255, 255, 255])  # Upper HSV threshold

try:
    while True:
        # Capture image from camera
        image = picam2.capture_array("main")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow('img', image_rgb)
        
        # Crop the image
        crop_img = image[210:270, 270:370]
	
        # Apply Gaussian blur - comment out option 1 or option 2
        # Option 1: blur cropped image
        blur = cv2.GaussianBlur(crop_img, (5, 5), 0)
        
        # Option 2: blur full image
        #blur = cv2.GaussianBlur(image, (5, 5), 0)

        # Convert to HSV color space
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # Show HSV values
        hsv_mean = np.mean(hsv, axis=(0, 1))  # Calculate the mean HSV
        print(f"Mean HSV values: {hsv_mean}")  # Print the mean HSV values

        # Threshold the image to keep only the selected color
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Show HSV and Mask images for debugging
        cv2.imshow('hsv', hsv)  # Show the HSV image
        cv2.imshow('mask', mask)  # Show the thresholded mask

        cv2.waitKey(1)
        
except KeyboardInterrupt:
    print('\nAll done')
