#!/usr/bin/env python3
"""
Create a simple test video with moving objects for testing
Run this locally: python create_test_video.py
Then commit test_video.mp4 to the repo
"""

import cv2
import numpy as np

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('test_video.mp4', fourcc, 30.0, (640, 480))

# Create 300 frames (10 seconds at 30 fps)
for frame_num in range(300):
    # Black background
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some moving rectangles (simulate people)
    # Rectangle 1 - moving left to right
    x1 = int((frame_num / 300) * 640)
    cv2.rectangle(frame, (x1, 100), (x1 + 50, 150), (0, 255, 0), -1)
    
    # Rectangle 2 - moving right to left
    x2 = int(640 - (frame_num / 300) * 640)
    cv2.rectangle(frame, (x2, 300), (x2 + 50, 350), (0, 0, 255), -1)
    
    # Add text showing frame number
    cv2.putText(frame, f'Frame: {frame_num}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    out.write(frame)

out.release()
print("Test video created: test_video.mp4")
