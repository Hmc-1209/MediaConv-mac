#include "image_converter.h"
#include <iostream>
#include <filesystem>
#include <opencv2/opencv.hpp>

// ==========================================================
// TODO: Reformat image function (e.g., PNG <-> JPEG <-> BMP)
// ==========================================================
extern "C" int reformat_image(const char* input_path, const char* output_ext) {
    if (!input_path || !output_ext) {
        std::cerr << "⚠ Error: input_path or output_ext is null!" << std::endl;
        return 1;
    }

    cv::Mat img = cv::imread(input_path, cv::IMREAD_UNCHANGED);
    if (img.empty()) {
        std::cerr << "⚠ Error: Cannot read image! " << input_path << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::filesystem::path output_file = input_file.parent_path() / (input_file.stem().string() + "." + output_ext);

    if (!cv::imwrite(output_file.string(), img)) {
        std::cerr << "⚠ Error: Cannot write image " << output_file << std::endl;
        return 1;
    }

    std::cout << "Image reformatted from " << input_path << " to " << output_file << std::endl;
    std::cout << "✓ Reformat complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Resize image function
// ==========================================================
extern "C" int resize_image(const char* input_path, int width, int height) {
    if (!input_path || width <= 0 || height <= 0) {
        std::cerr << "⚠ Error: input path or size is null!" << std::endl;
        return 1;
    }

    cv::Mat img = cv::imread(input_path, cv::IMREAD_UNCHANGED);
    if (img.empty()) {
        std::cerr << "⚠ Error: Cannot read image! " << input_path << std::endl;
        return 1;
    }

    cv::Mat resized;
    cv::resize(img, resized, cv::Size(width, height), 0, 0, cv::INTER_LINEAR);
    std::filesystem::path input_file(input_path);
    std::string output_name = input_file.stem().string() + "_resized" + std::to_string(width) + "x" +
            std::to_string(height) + input_file.extension().string();
    std::filesystem::path output_file = input_file.parent_path() / output_name;

    if (!cv::imwrite(output_file.string(), resized)) {
        std::cerr << "⚠ Error: Cannot write resized image " << output_file << std::endl;
        return 1;
    }

    std::cout << "Image resized to " << width << "x" << height << " and saved as " << output_file << std::endl;
    std::cout << "✓ Resize complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Crop image function
// ==========================================================
extern "C" int crop_image(const char* input_path, int start_x, int start_y, int width, int height) {
    if (!input_path || start_x < 0 || start_y < 0 || width <= 0 || height <= 0) {
        std::cerr << "⚠ Error: input path or size is null!" << std::endl;
        return 1;
    }

    cv::Mat img = cv::imread(input_path, cv::IMREAD_UNCHANGED);
    if (img.empty()) {
        std::cerr << "⚠ Error: Cannot read image! " << input_path << std::endl;
        return 1;
    }

    cv::Rect roi(start_x, start_y, width, height);
    if (roi.x + roi.width > img.cols || roi.y + roi.height > img.rows) {
        std::cerr << "⚠ Error: ROI out of image bounds!" << std::endl;
        return 1;
    }

    cv::Mat cropped = img(roi);
    std::filesystem::path input_file(input_path);
    std::string output_name = input_file.stem().string() + "_crop" + std::to_string(start_x) + "x" +
            std::to_string(start_y) + "_" + std::to_string(width) + "x" + std::to_string(height) +
            input_file.extension().string();
    std::filesystem::path output_file = input_file.parent_path() / output_name;

    if (!cv::imwrite(output_file.string(), cropped)) {
        std::cerr << "⚠ Error: Cannot write cropped image " << output_file << std::endl;
        return 1;
    }

    std::cout << "Image cropped (" << width << "x" << height << " at "
              << start_x << "," << start_y << ") and saved as " << output_file << std::endl;
    std::cout << "✓ Crop complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Rotate image function
// ==========================================================
extern "C" int rotate_image(const char* input_path, int angle) {
    if (!input_path) {
        std::cerr << "⚠ Error: input path is null!" << std::endl;
        return 1;
    }

    cv::Mat img = cv::imread(input_path, cv::IMREAD_UNCHANGED);
    if (img.empty()) {
        std::cerr << "⚠ Error: Cannot read image! " << input_path << std::endl;
        return 1;
    }

    cv::Mat rotated;
    if (angle == 90) {
        cv::rotate(img, rotated, cv::ROTATE_90_CLOCKWISE);
    } else if (angle == 180) {
        cv::rotate(img, rotated, cv::ROTATE_180);
    } else if (angle == 270) {
        cv::rotate(img, rotated, cv::ROTATE_90_COUNTERCLOCKWISE);
    } else {
        std::cerr << "⚠ Error: Unsupported rotation angle (" << angle << "). Use 90, 180, or 270." << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::string output_name = input_file.stem().string() + "_rot" + std::to_string(angle) +
            input_file.extension().string();
    std::filesystem::path output_file = input_file.parent_path() / output_name;

    if (!cv::imwrite(output_file.string(), rotated)) {
        std::cerr << "⚠ Error: Cannot write rotated image " << output_file << std::endl;
        return 1;
    }

    std::cout << "Image rotated " << angle << "° and saved as " << output_file << std::endl;
    std::cout << "✓ Rotate complete!" << std::endl;
    return 0;
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
