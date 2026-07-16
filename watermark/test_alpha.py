"""Test reverse-alpha + two-pass inpaint on difficult frame."""
import cv2
import numpy as np

ALPHA = 0.72
LOGO = 255.0

def text_mask(img, x, y, w, h):
    roi = img[y:y+h, x:x+w]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, m = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    m = cv2.dilate(m, kernel, iterations=1)
    full = np.zeros(img.shape[:2], np.uint8)
    full[y:y+h, x:x+w] = m
    return full

def reverse_alpha(img, mask, alpha=ALPHA):
    out = img.astype(np.float32)
    m = mask > 0
    for c in range(3):
        ch = out[:, :, c]
        ch[m] = (ch[m] - alpha * LOGO) / (1.0 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)

def remove(img):
    x, y, w, h = 438, 40, 210, 55
    m = text_mask(img, x, y, w, h)
    step1 = reverse_alpha(img, m)
    # Second pass: inpaint any leftover bright pixels
    gray = cv2.cvtColor(step1, cv2.COLOR_BGR2GRAY)
    roi = gray[y:y+h, x:x+w]
    leftover = (roi > 150).astype(np.uint8) * 255
    m2 = np.zeros(img.shape[:2], np.uint8)
    m2[y:y+h, x:x+w] = leftover
    if np.any(m2):
        step1 = cv2.inpaint(step1, m2, 3, cv2.INPAINT_TELEA)
    return step1

for name in ["frame0.png", "frame_mid.png"]:
    img = cv2.imread(rf"C:\Users\zakih\Desktop\watermark\frames\{name}")
    out = remove(img)
    cv2.imwrite(rf"C:\Users\zakih\Desktop\watermark\frames\alpha_{name}", out)
    print(f"saved alpha_{name}")
