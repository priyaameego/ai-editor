"""Test watermark removal approaches on sample frames."""
import cv2
import numpy as np

def detect_vizard_mask(img, margin_right=20, margin_top=10, search_w=250, search_h=100):
    """Detect white/semi-white Vizard.ai text in top-right corner."""
    h, w = img.shape[:2]
    x0 = max(0, w - search_w - margin_right)
    y0 = margin_top
    roi = img[y0 : y0 + search_h, x0 : w - margin_right]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Vizard text is bright; use adaptive threshold for varying backgrounds
    _, bright = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    # Also catch semi-transparent white (lighter than local median)
    local_med = cv2.medianBlur(gray, 15)
    semi = ((gray.astype(np.int16) - local_med.astype(np.int16)) > 25).astype(np.uint8) * 255
    combined = cv2.bitwise_or(bright, semi)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel, iterations=2)
    combined = cv2.dilate(combined, kernel, iterations=2)

    mask = np.zeros((h, w), dtype=np.uint8)
    mask[y0 : y0 + search_h, x0 : w - margin_right] = combined
    return mask

def remove_inpaint(img, mask, radius=5):
    return cv2.inpaint(img, mask, radius, cv2.INPAINT_TELEA)

def remove_reverse_alpha(img, mask, logo_val=255.0, alpha=0.85):
    """Only works if alpha is uniform and known — test for comparison."""
    out = img.astype(np.float32).copy()
    logo = logo_val
    for c in range(3):
        ch = out[:, :, c]
        m = mask > 0
        ch[m] = (ch[m] - alpha * logo) / (1.0 - alpha)
    return np.clip(out, 0, 255).astype(np.uint8)

for name in ["frame0.png", "frame_mid.png"]:
    path = rf"C:\Users\zakih\Desktop\watermark\frames\{name}"
    img = cv2.imread(path)
    mask = detect_vizard_mask(img)
    ys, xs = np.where(mask > 0)
    print(f"{name}: mask pixels={len(xs)}, bbox=({xs.min()},{ys.min()})-({xs.max()},{ys.max()})")

    inpainted = remove_inpaint(img, mask, radius=7)
    cv2.imwrite(rf"C:\Users\zakih\Desktop\watermark\frames\test_inpaint_{name}", inpainted)

    # Fixed bbox fallback (from analysis)
    fixed_mask = np.zeros(img.shape[:2], dtype=np.uint8)
    fixed_mask[38:95, 435:648] = 255
    inpaint_fixed = remove_inpaint(img, fixed_mask, radius=7)
    cv2.imwrite(rf"C:\Users\zakih\Desktop\watermark\frames\test_fixed_{name}", inpaint_fixed)

print("Saved test outputs")
