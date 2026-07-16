"""Analyze Vizard.ai watermark region in extracted frame."""
import cv2
import numpy as np

img = cv2.imread(r"C:\Users\zakih\Desktop\watermark\frames\frame0.png")
h, w = img.shape[:2]
print(f"Image size: {w}x{h}")

# Top-right region where watermark appears
roi = img[0:120, w - 280 : w]
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# White text threshold
_, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
ys, xs = np.where(mask > 0)
if len(xs):
    print(f"ROI local bbox: x={xs.min()}-{xs.max()}, y={ys.min()}-{ys.max()}")
    print(f"Global bbox: x={w - 280 + xs.min()}-{w - 280 + xs.max()}, y={ys.min()}-{ys.max()}")
    print(f"Mask pixels: {len(xs)}")

# Check if semi-transparent (compare two frames at same bg)
img2 = cv2.imread(r"C:\Users\zakih\Desktop\watermark\frames\frame_mid.png")
if img2 is not None:
    roi2 = img2[0:120, w - 280 : w]
    diff = cv2.absdiff(roi, roi2)
    print(f"ROI diff between frames (max): {diff.max()}, mean: {diff.mean():.2f}")

# Sample watermark pixel vs surrounding
for y, x in [(30, w - 150), (30, w - 50), (80, w - 150)]:
    b, g, r = img[y, x]
    print(f"Pixel at ({x},{y}): BGR=({b},{g},{r})")
