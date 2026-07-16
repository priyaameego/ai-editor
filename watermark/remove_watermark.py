"""
Remove Gemini static bottom-right watermark from video.

Uses inpainting on a dynamically calculated bounding box.

Usage:
  python remove_watermark.py [input.mp4] [output.mp4]
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np


def scale_box(width: int, height: int) -> tuple[int, int, int, int]:
    # Tight box that safely encompasses the entire star including outer tips
    w = int(width * 0.05)
    h = int(width * 0.05)
    x = int(width * 0.875)
    y = int(height * 0.785)
    return x, y, w, h


def build_watermark_mask(frames: list[np.ndarray], box: tuple[int, int, int, int], thresh: float = 8.0) -> np.ndarray:
    """Return an elliptical mask to tightly cover the star including its tips, preserving extreme corner pixels."""
    x, y, w, h = box
    mask = np.zeros((h, w), dtype=np.uint8)
    cx, cy = w // 2, h // 2
    # Draw a filled ellipse to cover the star and its thick rays
    cv2.ellipse(mask, (cx, cy), (w // 2, h // 2), 0, 0, 360, 255, -1)
    # Dilate slightly to cover glowing edges completely
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.dilate(mask, kernel, iterations=1)
    return mask


def apply_patch_masked(frame: np.ndarray, mask: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    x, y, w, h = box
    out = frame.copy()
    roi = out[y : y + h, x : x + w]
    # Use cv2.inpaint to remove the watermark since the background might be static
    inpainted = cv2.inpaint(roi, mask.astype(np.uint8), 3, cv2.INPAINT_NS)
    out[y : y + h, x : x + w] = inpainted
    return out


def cleanup_leftover(frame: np.ndarray, box: tuple[int, int, int, int]) -> np.ndarray:
    x, y, w, h = box
    roi = frame[y : y + h, x : x + w]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)
    if not np.any(mask):
        return frame
    full = np.zeros(frame.shape[:2], dtype=np.uint8)
    full[y : y + h, x : x + w] = mask
    return cv2.inpaint(frame, full, 3, cv2.INPAINT_NS)


def process_video(input_path: str, output_path: str) -> None:
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    box = scale_box(width, height)
    x, y, w, h = box

    print(f"Input: {width}x{height} @ {fps:.1f} fps")
    print(f"Watermark box: x={x} y={y} w={w} h={h}")

    print("Pass 1/2: reading frames...")
    frames: list[np.ndarray] = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(frame)

    cap.release()
    total = len(frames)
    print(f"  {total} frames loaded")

    if total == 0:
        raise RuntimeError("No frames read from video.")

    mask = build_watermark_mask([frames[0]], box)

    print("Pass 2/2: applying masked removal...")
    tmp = Path(tempfile.gettempdir()) / "watermark_removed_noaudio.mp4"
    writer = cv2.VideoWriter(str(tmp), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    for i, frame in enumerate(frames):
        out = apply_patch_masked(frame, mask, box)
        out = cleanup_leftover(out, box)
        writer.write(out)
        if (i + 1) % 120 == 0 or i + 1 == total:
            print(f"  {i + 1}/{total} frames", flush=True)

    writer.release()

    print("Merging audio with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(tmp),
        "-i", str(input_path),
        "-map", "0:v:0", "-map", "1:a:0?",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", str(output_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr)
            raise RuntimeError("ffmpeg failed")
    except FileNotFoundError:
        print("Warning: ffmpeg not found in PATH! Falling back to local ffmpeg.exe.")
        local_ffmpeg = Path(__file__).parent / "ffmpeg.exe"
        if not local_ffmpeg.exists():
             raise RuntimeError(f"ffmpeg not found in PATH and local {local_ffmpeg} does not exist.")
        cmd[0] = str(local_ffmpeg)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr)
            raise RuntimeError("local ffmpeg failed")

    tmp.unlink(missing_ok=True)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    inp = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input.mp4")
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output_no_watermark.mp4")
    
    if not inp.exists():
        print(f"Error: Input file {inp} not found!")
        sys.exit(1)
        
    process_video(str(inp), str(out))
