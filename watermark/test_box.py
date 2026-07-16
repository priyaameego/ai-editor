import cv2
import numpy as np

def scale_box(width: int, height: int) -> tuple[int, int, int, int]:
    # Gemini star is small and square. Use a tight 6% box.
    w = int(width * 0.06)
    h = int(width * 0.06)  # Keep it square
    x = width - w - int(width * 0.015)
    y = height - h - int(height * 0.025)
    return x, y, w, h

video_path = r"c:\Users\Priya\Documents\watermark\watermark\outputs\clean_1685a175-86fe-4b57-a520-b931fb3eaee9.mp4"
cap = cv2.VideoCapture(video_path)
ok, frame = cap.read()
if ok:
    h, w = frame.shape[:2]
    bx, by, bw, bh = scale_box(w, h)
    
    # Draw green box
    cv2.rectangle(frame, (bx, by), (bx+bw, by+bh), (0, 255, 0), 2)
    cv2.imwrite("debug_box.png", frame)
    
    print(f"Video: {w}x{h}, Box: {bx}, {by}, {bw}, {bh}")
else:
    print("Could not read video")
