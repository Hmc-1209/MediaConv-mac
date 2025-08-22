#include "video_converter.h"
#include <iostream>
#include <filesystem>

// ==========================================================
// TODO: Reformat video function (e.g., MP4 <-> AVI <-> MKV)
// ==========================================================
extern "C" int reformat_video(const char* input_path, const char* output_ext, int overwrite) {
    if (!input_path || !output_ext) {
        std::cerr << "⚠ Error: input_path or output_ext is unavailable!" << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::string input_ext = input_file.extension().string();
    if (!input_ext.empty() && input_ext[0] == '.') input_ext = input_ext.substr(1);

    if (input_ext == output_ext) {
        std::cerr << "⚠ Error: Input and output formats are the same (" << input_ext << ")!" << std::endl;
        return 1;
    }

    std::filesystem::path output_file = input_file.parent_path() / (input_file.stem().string() + "." + output_ext);
    std::string cmd = "ffmpeg -hide_banner -loglevel error -y -i \"" + input_file.string() +
                      "\" -c:v libx264 -c:a aac \"" + output_file.string() + "\"";

    int ret = std::system(cmd.c_str());
    if (ret != 0) {
        std::cerr << "⚠ Error: FFmpeg failed to convert video!" << std::endl;
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

    std::cout << "Video reformatted from " << input_file << " to " << output_file << std::endl;
    std::cout << "✓ Reformat complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Resize video function
// ==========================================================
extern "C" int resize_video(const char* input_path, int width, int height, int overwrite) {
    if (!input_path || width <= 0 || height <= 0) {
        std::cerr << "⚠ Error: input_path is unavailable!" << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::string input_ext = input_file.extension().string();
    if (!input_ext.empty() && input_ext[0] == '.') input_ext = input_ext.substr(1);

    std::filesystem::path output_file = input_file.parent_path() /
                                        (input_file.stem().string() + "_resized." + input_ext);

    std::string cmd = "ffmpeg -hide_banner -loglevel error -y -i \"" + input_file.string() +
                      "\" -vf scale=" + std::to_string(width) + ":" + std::to_string(height) +
                      " -c:a copy \"" + output_file.string() + "\"";

    int ret = std::system(cmd.c_str());
    if (ret != 0) {
        std::cerr << "⚠ Error: FFmpeg failed to resize video!" << std::endl;
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

    std::cout << "Video resized to " << width << "x" << height << " → " << output_file << std::endl;
    std::cout << "✓ Resize complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Crop video function
// ==========================================================
extern "C" void crop_video() {
    std::cout << "Video conversion function called!" << std::endl;
}

// ==========================================================
// TODO: Rotate video function
// ==========================================================
extern "C" void rotate_video() {
    std::cout << "Video conversion function called!" << std::endl;
}

// ==========================================================
// TODO: Flip video function (horizontal/vertical)
// ==========================================================
extern "C" void flip_video() {
    std::cout << "Video conversion function called!" << std::endl;
}

// ==========================================================
// TODO: Adjust brightness/contrast function
// ==========================================================
extern "C" void adjust_brightness_video() {
    std::cout << "Video conversion function called!" << std::endl;
}