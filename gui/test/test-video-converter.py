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
last_generated_files = ["./vids/bbb_short.mp4", "./vids/bbb_short_resized.mkv", "./vids/bbb_short_cropped.mkv", "./vids/bbb_short_rotated.mkv",
                        "./vids/bbb_short_flipped.mkv", "./vids/bbb_short_adj_c1.200000_b0.100000.mkv"]
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

# ----------------------------------
# Crop video to 10x10~100x100
# ----------------------------------
print("--------------Crop Video---------------")
print(f"Cropping bbb_short.mkv at x=10, y=10, width=100, height=100...")
if video_lib.crop_video(b"./vids/bbb_short.mkv", 10, 10, 100, 100, 0):
    print("Please checkout the log to see the issue.")

# ----------------------------------
# Rotate video 90° clockwise
# ----------------------------------
print("--------------Rotate Video---------------")
print(f"Rotating bbb_short.mkv by 90 degrees...")
if video_lib.rotate_video(b"./vids/bbb_short.mkv", 90, 0):
    print("Please checkout the log to see the issue.")

# ----------------------------------
# Flip video horizontally
# ----------------------------------
print("--------------Flip Video---------------")
print(f"Flipping bbb_short.mkv horizontally...")
if video_lib.flip_video(b"./vids/bbb_short.mkv", 1, 0):  # 0=vertical, 1=horizontal
    print("Please checkout the log to see the issue.")

# ----------------------------------
# Adjust video brightness & contrast
# ----------------------------------
print("--------------Adjust Video---------------")
print(f"Adjusting bbb_short.mkv contrast=1.2, brightness=0.1...")
if video_lib.adjust_brightness_video(b"./vids/bbb_short.mkv", ctypes.c_double(1.2), ctypes.c_double(0.1), False):
    print("Please checkout the log to see the issue.")