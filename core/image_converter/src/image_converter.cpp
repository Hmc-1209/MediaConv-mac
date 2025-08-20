#include "image_converter.h"
#include <iostream>
#include <filesystem>
#include <opencv2/opencv.hpp>

// ==========================================================
// TODO: Reformat image function (e.g., PNG <-> JPEG <-> BMP)
// ==========================================================
extern "C" int reformat_image(const char* input_path, const char* output_ext, int overwrite) {
    if (!input_path || !output_ext) {
        std::cerr << "⚠ Error: input_path or output_ext is unavailable!" << std::endl;
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
    if (overwrite) {
        try {
            std::filesystem::remove(input_file);
            std::cout << "⚠ Original file " << input_file << " removed after generating " << output_file << std::endl;
        } catch (const std::filesystem::filesystem_error& e) {
            std::cerr << "⚠ Error removing original file: " << e.what() << std::endl;
        }
    }

    std::cout << "Image reformatted from " << input_path << " to " << output_file << std::endl;
    std::cout << "✓ Reformat complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Resize image function
// ==========================================================
extern "C" int resize_image(const char* input_path, int width, int height, int overwrite) {
    if (!input_path || width <= 0 || height <= 0) {
        std::cerr << "⚠ Error: input path or size is unavailable!" << std::endl;
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
    std::filesystem::path output_file  = input_file;
    if (!overwrite) {
        std::string output_name = input_file.stem().string() + "_resized" + std::to_string(width) + "x" +
                                  std::to_string(height) + input_file.extension().string();
        output_file = input_file.parent_path() / output_name;
    }

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
extern "C" int crop_image(const char* input_path, int start_x, int start_y, int width, int height, int overwrite) {
    if (!input_path || start_x < 0 || start_y < 0 || width <= 0 || height <= 0) {
        std::cerr << "⚠ Error: input path or size is unavailable!" << std::endl;
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
    std::filesystem::path output_file = input_file;
    if (!overwrite) {
        std::string output_name = input_file.stem().string() + "_crop" + std::to_string(start_x) + "x" +
                                  std::to_string(start_y) + "_" + std::to_string(width) + "x" +
                                  std::to_string(height) + input_file.extension().string();
        output_file = input_file.parent_path() / output_name;
    }


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
extern "C" int rotate_image(const char* input_path, int angle, int overwrite) {
    if (!input_path) {
        std::cerr << "⚠ Error: input path is unavailable!" << std::endl;
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
    std::filesystem::path output_file = input_file;
    if (!overwrite) {
        std::string output_name = input_file.stem().string() + "_rot" + std::to_string(angle) +
                                  input_file.extension().string();
        output_file = input_file.parent_path() / output_name;
    }

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
extern "C" int flip_image(const char* input_path, int direction, int overwrite) {
    if (!input_path) {
        std::cerr << "⚠ Error: input path or direction is unavailable!" << std::endl;
        return 1;
    }

    cv::Mat img = cv::imread(input_path, cv::IMREAD_UNCHANGED);
    if (img.empty()) {
        std::cerr << "⚠ Error: Cannot read image! " << input_path << std::endl;
        return 1;
    }

    cv::Mat flipped;
    if (direction == 0) {
        cv::flip(img, flipped, 0);
    } else if (direction == 1) {
        cv::flip(img, flipped, 1);
    } else {
        std::cerr << "⚠ Error: Unsupported direction (" << direction << "). Use 0(vertical) or 1(horizontal)."
                  << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::filesystem::path output_file = input_file;
    if (!overwrite) {
        std::string output_name = input_file.stem().string() + "_flip" + (direction == 0 ? "H" : "V") +
                                  input_file.extension().string();
        output_file = input_file.parent_path() / output_name;
    }

    if (!cv::imwrite(output_file.string(), flipped)) {
        std::cerr << "⚠ Error: Cannot write flipped image " << output_file << std::endl;
        return 1;
    }

    std::cout << "Image flipped " << (direction == 0 ? "horizontally" : "vertically") << " and saved as "
              << output_file << std::endl;
    std::cout << "✓ Flip complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Adjust brightness/contrast function
// ==========================================================
extern "C" int adjust_brightness_image(const char* input_path, double alpha, int beta, bool overwrite) {
    if (!input_path) {
        std::cerr << "⚠ Error: input path is unavailable!" << std::endl;
        return 1;
    }

    cv::Mat img = cv::imread(input_path, cv::IMREAD_UNCHANGED);
    if (img.empty()) {
        std::cerr << "⚠ Error: Cannot read image! " << input_path << std::endl;
        return 1;
    }

    cv::Mat adjusted;
    img.convertTo(adjusted, -1, alpha, beta);
    std::filesystem::path input_file(input_path);
    std::filesystem::path output_file = input_file;
    if (!overwrite) {
        std::string output_name = input_file.stem().string() + "_adj_c" + std::to_string(alpha) +
                                  "_b" + std::to_string(beta) + input_file.extension().string();
        output_file = input_file.parent_path() / output_name;
    }

    if (!cv::imwrite(output_file.string(), adjusted)) {
        std::cerr << "⚠ Error: Cannot write adjusted image " << output_file << std::endl;
        return 1;
    }

    std::cout << "Image adjusted (contrast=" << alpha << ", brightness=" << beta << ") and saved as " << output_file
              << std::endl;
    std::cout << "✓ Adjust complete!" << std::endl;
    return 0;
}
