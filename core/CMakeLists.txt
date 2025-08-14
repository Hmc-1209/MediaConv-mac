cmake_minimum_required(VERSION 4.0)
project(MediaConv)
set(CMAKE_CXX_STANDARD 20)

# ============================
# library: image_converter
# ============================
add_library(image_converter SHARED
        image_converter/src/image_converter.cpp
)
target_include_directories(image_converter PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/image_converter/include
)

# ============================
# library: video_converter
# ============================
add_library(video_converter SHARED
        video_converter/src/video_converter.cpp
)
target_include_directories(video_converter PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/video_converter/include
)