import urllib.request
import zipfile
import os
import shutil

print("Downloading ffmpeg...")
url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
zip_path = "ffmpeg.zip"

urllib.request.urlretrieve(url, zip_path)
print("Downloaded. Extracting...")

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall("ffmpeg_extracted")

# Find the ffmpeg.exe inside the extracted folder
for root, dirs, files in os.walk("ffmpeg_extracted"):
    if "ffmpeg.exe" in files:
        ffmpeg_exe_path = os.path.join(root, "ffmpeg.exe")
        shutil.copy(ffmpeg_exe_path, "ffmpeg.exe")
        print("Copied ffmpeg.exe to project root.")
        break

# Cleanup
if os.path.exists("ffmpeg.zip"):
    os.remove("ffmpeg.zip")
if os.path.exists("ffmpeg_extracted"):
    shutil.rmtree("ffmpeg_extracted")

print("Done!")
