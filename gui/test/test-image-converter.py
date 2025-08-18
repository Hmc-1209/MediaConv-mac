# Python test: check image converter functioning

import ctypes
import os

build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../core/build"))

# ---------------------------
# Initialize function return
# ---------------------------
image_lib = ctypes.CDLL(os.path.join(build_dir, "libimage_converter.dylib"))
image_lib.reformat_image.restype = int
image_lib.resize_image.restype = None
image_lib.crop_image.restype = None
image_lib.rotate_image.restype = None
image_lib.flip_image.restype = None
image_lib.adjust_brightness_image.restype = None
image_lib.batch_process_image.restype = None

# ---------------------------
# Remove last generated files
# ---------------------------
print("\n===================================")
print("Removing last generated files -->")
print("===================================")
last_generated_files = ["./pics/Lenna.png"]
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
if image_lib.reformat_image(b"./pics/Lenna.jpg", b"png"):
  print("Please checkout the log to see the issue.")