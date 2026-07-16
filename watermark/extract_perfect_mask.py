import cv2
import numpy as np

video_path = r"c:\Users\Priya\Documents\watermark\watermark\outputs\clean_1685a175-86fe-4b57-a520-b931fb3eaee9.mp4"
cap = cv2.VideoCapture(video_path)

frames = []
h, w = 720, 1280
box_w = int(w * 0.035)
box_h = int(h * 0.06)
box_x = int(w * 0.885)
box_y = int(h * 0.80)

# Read 50 frames
for _ in range(50):
    ok, frame = cap.read()
    if not ok: break
    frames.append(frame[box_y:box_y+box_h, box_x:box_x+box_w])

cap.release()

stack = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames])
std_dev = np.std(stack, axis=0)
mean_img = np.mean(stack, axis=0)

# The star is static (low std_dev) and bright (high mean)
# Let's see if we can isolate it
mask = ((std_dev < 10) & (mean_img > 130)).astype(np.uint8) * 255

# Dilate slightly to cover edges
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
mask_dilated = cv2.dilate(mask, kernel, iterations=1)

cv2.imwrite("debug_perfect_mask.png", mask_dilated)

# Let's see how many pixels the mask covers
print(f"Mask pixels: {np.count_nonzero(mask_dilated)}")
