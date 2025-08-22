# Python test: check video converter functioning

import ctypes
import os

build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../core/build"))

# ---------------------------
# Initialize function return
# ---------------------------
video_lib = ctypes.CDLL(os.path.join(build_dir, "libvideo_converter.dylib"))
video_lib.reformat_video.restype = int
video_lib.resize_video.restype = int
video_lib.crop_video.restype = None
video_lib.rotate_video.restype = None
video_lib.flip_video.restype = None
video_lib.adjust_brightness_video.restype = None

# ---------------------------
# Remove last generated files
# ---------------------------
print("\n===================================")
print("Removing last generated files -->")
print("===================================")
last_generated_files = ["./vids/bbb_short.mp4"]
for path in last_generated_files:
  if os.path.exists(path):
    os.remove(path)
    print("File", path, "removed.")
  else:
    print("File", path, "not exist.")
print("\n===================================")
print("Beginning Video Converter test -->")
print("===================================")

# ----------------------------------
# Reformat video to different format
# ----------------------------------
print("-------------Reformat Video--------------")
print(f"Reformatting bbb_short.mkv to bbb_short.mp4...")
if video_lib.reformat_video(b"./vids/bbb_short.mkv", b"mp4", 0):
  print("Please checkout the log to see the issue.")

# ----------------------------------
# Resize video to 200x200px
# ----------------------------------
print("--------------Resize Video---------------")
print(f"Resizing bbb_short.mkv to 200x200px...")
if video_lib.resize_video(b"./vids/bbb_short.mkv", 200, 200, 0):
  print("Please checkout the log to see the issue.")