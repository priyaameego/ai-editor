import cv2
import numpy as np

video_path = r"c:\Users\Priya\Documents\watermark\watermark\outputs\clean_1685a175-86fe-4b57-a520-b931fb3eaee9.mp4"
cap = cv2.VideoCapture(video_path)
ok, frame = cap.read()
if ok:
    h, w = frame.shape[:2]
    # Crop bottom-right 25%
    roi = frame[int(h*0.75):h, int(w*0.75):w]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Find the brightest pixel in this region
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)
    
    # max_loc is (x, y) relative to ROI
    global_x = int(w*0.75) + max_loc[0]
    global_y = int(h*0.75) + max_loc[1]
    
    print(f"Brightest pixel at global ({global_x}, {global_y}) with value {max_val}")
    
    # Let's also check where pixels are > 180
    ys, xs = np.where(gray > 180)
    if len(xs) > 0:
        print(f"Pixels > 180 bounding box in ROI: X[{min(xs)}-{max(xs)}], Y[{min(ys)}-{max(ys)}]")
        print(f"Global Box: X[{int(w*0.75)+min(xs)}-{int(w*0.75)+max(xs)}], Y[{int(h*0.75)+min(ys)}-{int(h*0.75)+max(ys)}]")
    else:
        print("No pixels > 180 in ROI")
else:
    print("Could not read video")
