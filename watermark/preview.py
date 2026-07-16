"""Quick preview of fixed-box removal on two frames."""
import cv2
import numpy as np
from pathlib import Path
from remove_watermark import scale_box, build_watermark_mask, apply_patch_masked

if __name__ == "__main__":
    frames_dir = Path("frames")
    
    if not frames_dir.exists():
        print(f"Warning: {frames_dir} directory not found. Please create it and add 'frame0.png' and 'frame_mid.png' for previewing.")
    else:
        for name in ["frame0.png", "frame_mid.png"]:
            img_path = frames_dir / name
            if not img_path.exists():
                print(f"File {img_path} not found. Skipping.")
                continue
                
            img = cv2.imread(str(img_path))
            h, w = img.shape[:2]
            box = scale_box(w, h)
            mask = build_watermark_mask([img], box)
            out = apply_patch_masked(img, mask, box)
            
            out_path = frames_dir / f"preview_{name}"
            cv2.imwrite(str(out_path), out)
            n = np.count_nonzero(mask)
            print(f"{name}: mask pixels={n}, box={box}")
