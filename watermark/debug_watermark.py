import cv2
import numpy as np
import sys
import os

video_path = r"c:\Users\Priya\Documents\watermark\watermark\outputs\clean_1685a175-86fe-4b57-a520-b931fb3eaee9.mp4"
cap = cv2.VideoCapture(video_path)
ok, frame = cap.read()
if not ok:
    print("Could not read video")
    sys.exit(1)

height, width = frame.shape[:2]
print(f"Video size: {width}x{height}")

w = int(width * 0.15)
h = int(height * 0.15)
x = width - w - int(width * 0.02)
y = height - h - int(height * 0.02)
print(f"Box: x={x}, y={y}, w={w}, h={h}")

roi = frame[y:y+h, x:x+w]
cv2.imwrite("debug_roi.png", roi)

gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
_, mask150 = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
cv2.imwrite("debug_mask150.png", mask150)

# Let's find the brightest spot (the star) using a higher threshold
_, mask220 = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
cv2.imwrite("debug_mask220.png", mask220)

# What if we use temporal processing to find the static part?
frames = []
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
for i in range(30):
    ok, f = cap.read()
    if not ok: break
    frames.append(f[y:y+h, x:x+w])

stack = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames])
std_dev = np.std(stack, axis=0)
cv2.imwrite("debug_std_dev.png", (std_dev * 10).astype(np.uint8))

mean_img = np.mean(stack, axis=0)
cv2.imwrite("debug_mean.png", mean_img.astype(np.uint8))

cap.release()
print("Done extracting debug images.")
