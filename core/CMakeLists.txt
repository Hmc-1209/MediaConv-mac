cmake_minimum_required(VERSION 4.0)
project(MediaConv)
set(CMAKE_CXX_STANDARD 20)

# Set OpenCV directory
set(OpenCV_DIR "/Users/danny/opencv-static/opencv/opencv_static/share/opencv4")
find_package(OpenCV REQUIRED)

# ============================
# library: image_converter
# ============================
add_library(image_converter SHARED
        image_converter/src/image_converter.cpp
)
target_include_directories(image_converter PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/image_converter/include
        ${OpenCV_INCLUDE_DIRS}
)
target_link_libraries(image_converter PRIVATE ${OpenCV_LIBS})

# ============================
# library: video_converter
# ============================
add_library(video_converter SHARED
        video_converter/src/video_converter.cpp
)
target_include_directories(video_converter PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/video_converter/include
)
# ============================
# installation rules
# ============================
install(TARGETS image_converter video_converter
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin
        PUBLIC_HEADER DESTINATION include
)