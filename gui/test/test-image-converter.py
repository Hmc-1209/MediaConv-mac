# Python test: check image converter functioning

import ctypes
import os

build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../core/build"))

# ---------------------------
# Initialize function return
# ---------------------------
image_lib = ctypes.CDLL(os.path.join(build_dir, "libimage_converter.dylib"))
image_lib.reformat_image.restype = int
image_lib.resize_image.restype = int
image_lib.crop_image.restype = int
image_lib.rotate_image.restype = int
image_lib.flip_image.restype = int
image_lib.adjust_brightness_image.restype = int

# ---------------------------
# Remove last generated files
# ---------------------------
print("\n===================================")
print("Removing last generated files -->")
print("===================================")
last_generated_files = ["./pics/Lenna.png", "./pics/Lenna_resized100x100.jpg", "./pics/Lenna_crop50x50_100x100.jpg", "./pics/Lenna_rot90.jpg",
                        "./pics/Lenna_flipV.jpg", "./pics/Lenna_adj_c1.600000_b30.jpg"]
for path in last_generated_files:
  if os.path.exists(path):
    os.remove(path)
    print("File", path, "removed.")
  else:
    print("File", path, "not exist.")
print("\n===================================")
print("Beginning Image Converter test -->")
print("===================================")

# ---------------------------
# Reformat image to PNG file
# ---------------------------
print("-------------Reformat--------------")
print("Reformatting Lenna.jpg to Lenna.png...")
if image_lib.reformat_image(b"./pics/Lenna.jpg", b"png", 0):
  print("Please checkout the log to see the issue.")

# ---------------------------
# Resize image to 100 * 100
# ---------------------------
print("--------------Resize---------------")
print("Resizing Lenna.jpg to 100*100px...")
if image_lib.resize_image(b"./pics/Lenna.jpg", 100, 100, 0):
  print("Please checkout the log to see the issue.")

# ---------------------------
# Crop image to 50x50~100x100
# ---------------------------
print("---------------Crop----------------")
print("Cropping Lenna.jpg to 50x50~100x100...")
if image_lib.crop_image(b"./pics/Lenna.jpg", 50, 50, 100, 100, 0):
  print("Please checkout the log to see the issue.")

# ---------------------------
# Rotate image 90° clockwise
# ---------------------------
print("--------------Rotate---------------")
print("Rotating Lenna.jpg 90° clockwise...")
if image_lib.rotate_image(b"./pics/Lenna.jpg", 90, 0):
  print("Please checkout the log to see the issue.")

# ---------------------------
# Flip image horizontally
# ---------------------------
print("---------------Flip----------------")
print("Flipping Lenna.jpg horizontally...")
if image_lib.flip_image(b"./pics/Lenna.jpg", 1, 0):
  print("Please checkout the log to see the issue.")

# ----------------------------------
# Adjust image brightness & contrast
# ----------------------------------
print("--------------Adjust---------------")
print("Adjusting Lenna.jpg's brightness and contrast...")
if image_lib.adjust_brightness_image(b"./pics/Lenna.jpg", ctypes.c_double(1.6), 30, 0):
  print("Please checkout the log to see the issue.")