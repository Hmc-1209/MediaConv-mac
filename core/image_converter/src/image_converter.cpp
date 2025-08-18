#include "image_converter.h"
#include <iostream>
#include <filesystem>
#include <opencv2/opencv.hpp>

// ==========================================================
// TODO: Reformat image function (e.g., PNG <-> JPEG <-> BMP)
// ==========================================================
extern "C" int reformat_image(const char* input_path, const char* output_ext) {
    if (!input_path || !output_ext) {
        std::cerr << "X) Error: input_path or output_ext is null!" << std::endl;
        return 1;
    }

    cv::Mat img = cv::imread(input_path, cv::IMREAD_UNCHANGED);
    if (img.empty()) {
        std::cerr << "X) Error: Cannot read image! " << input_path << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::filesystem::path output_file = input_file.parent_path() / (input_file.stem().string() + "." + output_ext);

    if (!cv::imwrite(output_file.string(), img)) {
        std::cerr << "X) Error: Cannot write image " << output_file << std::endl;
        return 1;
    }

    std::cout << "Image reformatted from " << input_path << " to " << output_file << std::endl;
    std::cout << "O) Reformat complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Resize image function
// ==========================================================
extern "C" void resize_image() {
    std::cout << "Image conversion function called!" << std::endl;
}

// ==========================================================
// TODO: Crop image function
// ==========================================================
extern "C" void crop_image() {
    std::cout << "Image conversion function called!" << std::endl;
}

// ==========================================================
// TODO: Rotate image function
// ==========================================================
extern "C" void rotate_image() {
    std::cout << "Image conversion function called!" << std::endl;
}

// ==========================================================
// TODO: Flip image function (horizontal/vertical)
// ==========================================================
extern "C" void flip_image() {
    std::cout << "Image conversion function called!" << std::endl;
}

// ==========================================================
// TODO: Adjust brightness/contrast function
// ==========================================================
extern "C" void adjust_brightness_image() {
    std::cout << "Image conversion function called!" << std::endl;
}

// ==========================================================
// TODO: Batch process multiple images function
// ==========================================================
extern "C" void batch_process_image() {
    std::cout << "Image conversion function called!" << std::endl;
}
