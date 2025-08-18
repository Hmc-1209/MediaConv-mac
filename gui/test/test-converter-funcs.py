# Temporary Python test: check that image/video functions are exported and callable
# Only for initial testing

import ctypes
import os

build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../core/build"))

image_lib = ctypes.CDLL(os.path.join(build_dir, "libimage_converter.dylib"))
video_lib = ctypes.CDLL(os.path.join(build_dir, "libvideo_converter.dylib"))

image_lib.reformat_image.restype = None
image_lib.resize_image.restype = None
image_lib.crop_image.restype = None
image_lib.rotate_image.restype = None
image_lib.flip_image.restype = None
image_lib.adjust_brightness_image.restype = None
image_lib.batch_process_image.restype = None

video_lib.reformat_video.restype = None
video_lib.resize_video.restype = None
video_lib.crop_video.restype = None
video_lib.rotate_video.restype = None
video_lib.flip_video.restype = None
video_lib.adjust_brightness_video.restype = None
video_lib.batch_process_video.restype = None

print("Testing image_converter:")
image_lib.reformat_image()
image_lib.resize_image()
image_lib.crop_image()
image_lib.rotate_image()
image_lib.flip_image()
image_lib.adjust_brightness_image()
image_lib.batch_process_image()

print("\nTesting video_converter:")
video_lib.reformat_video()
video_lib.resize_video()
video_lib.crop_video()
video_lib.rotate_video()
video_lib.flip_video()
video_lib.adjust_brightness_video()
video_lib.batch_process_video()
