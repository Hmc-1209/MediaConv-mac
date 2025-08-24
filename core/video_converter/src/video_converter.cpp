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
extern "C" int crop_video(const char* input_path, int start_x, int start_y, int width, int height, int overwrite) {
    if (!input_path || start_x < 0 || start_y < 0 || width <= 0 || height <= 0) {
        std::cerr << "⚠ Error: input_path or crop area/size is unavailable!" << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::string input_ext = input_file.extension().string();
    if (!input_ext.empty() && input_ext[0] == '.') input_ext = input_ext.substr(1);

    std::filesystem::path output_file = input_file.parent_path() /
                                        (input_file.stem().string() + "_cropped." + input_ext);

    std::string cmd = "ffmpeg -hide_banner -loglevel error -y -i \"" + input_file.string() +
                      "\" -vf crop=" + std::to_string(width) + ":" + std::to_string(height) +
                      ":" + std::to_string(start_x) + ":" + std::to_string(start_y) +
                      " -c:a copy \"" + output_file.string() + "\"";

    int ret = std::system(cmd.c_str());
    if (ret != 0) {
        std::cerr << "⚠ Error: FFmpeg failed to crop video!" << std::endl;
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

    std::cout << "Video cropped to " << width << "x" << height << " → " << output_file << std::endl;
    std::cout << "✓ Crop complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Rotate video function
// ==========================================================
extern "C" int rotate_video(const char* input_path, int angle, int overwrite) {
    if (!input_path) {
        std::cerr << "⚠ Error: input_path is unavailable!" << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::string input_ext = input_file.extension().string();
    if (!input_ext.empty() && input_ext[0] == '.') input_ext = input_ext.substr(1);

    std::filesystem::path output_file = input_file.parent_path() /
                                        (input_file.stem().string() + "_rotated." + input_ext);

    std::string vf_filter;

    if (angle == 90) {
        vf_filter = "transpose=1";
    } else if (angle == 180) {
        vf_filter = "transpose=1,transpose=1";
    } else if (angle == 270) {
        vf_filter = "transpose=1,transpose=1,transpose=1";
    } else {
        std::cerr << "⚠ Error: unsupported rotation angle (" << angle << ")!" << std::endl;
        return 1;
    }

    std::string cmd = "ffmpeg -hide_banner -loglevel error -y -i \"" + input_file.string() +
                      "\" -vf \"" + vf_filter + "\" -c:a copy \"" + output_file.string() + "\"";

    int ret = std::system(cmd.c_str());
    if (ret != 0) {
        std::cerr << "⚠ Error: FFmpeg failed to rotate video!" << std::endl;
        return 1;
    }

    if (overwrite) {
        try {
            std::filesystem::remove(input_file);
            std::cout << "⚠ Original file " << input_file << " removed after generating "
                      << output_file << std::endl;
        } catch (const std::filesystem::filesystem_error& e) {
            std::cerr << "⚠ Error removing original file: " << e.what() << std::endl;
        }
    }

    std::cout << "Video rotated " << angle << "° → " << output_file << std::endl;
    std::cout << "✓ Rotate complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Flip video function (horizontal/vertical)
// ==========================================================
extern "C" int flip_video(const char* input_path, int direction, int overwrite) {
    if (!input_path) {
        std::cerr << "⚠ Error: input_path is unavailable!" << std::endl;
        return 1;
    }

    if (direction != 0 && direction != 1) {
        std::cerr << "⚠ Error: Unsupported direction (" << direction
                  << "). Use 0 (vertical) or 1 (horizontal)." << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::string input_ext = input_file.extension().string();
    if (!input_ext.empty() && input_ext[0] == '.') input_ext = input_ext.substr(1);

    std::filesystem::path output_file = input_file.parent_path() /
                                        (input_file.stem().string() + "_flipped." + input_ext);

    std::string vf_filter = (direction == 0) ? "vflip" : "hflip";
    std::string cmd = "ffmpeg -hide_banner -loglevel error -y -i \"" + input_file.string() +
                      "\" -vf " + vf_filter + " -c:a copy \"" + output_file.string() + "\"";

    int ret = std::system(cmd.c_str());
    if (ret != 0) {
        std::cerr << "⚠ Error: FFmpeg failed to flip video!" << std::endl;
        return 1;
    }

    if (overwrite) {
        try {
            std::filesystem::remove(input_file);
            std::cout << "⚠ Original file " << input_file
                      << " removed after generating " << output_file << std::endl;
        } catch (const std::filesystem::filesystem_error& e) {
            std::cerr << "⚠ Error removing original file: " << e.what() << std::endl;
        }
    }

    std::cout << "Video flipped " << (direction == 0 ? "vertically" : "horizontally")
              << " → " << output_file << std::endl;
    std::cout << "✓ Flip complete!" << std::endl;
    return 0;
}

// ==========================================================
// TODO: Adjust brightness/contrast function
// ==========================================================
extern "C" int adjust_brightness_video(const char* input_path, double alpha, double beta, bool remove_original) {
    if (!input_path) {
        std::cerr << "⚠ Error: input path is unavailable!" << std::endl;
        return 1;
    }

    std::filesystem::path input_file(input_path);
    std::string input_ext = input_file.extension().string();
    if (!input_ext.empty() && input_ext[0] == '.') input_ext = input_ext.substr(1);

    std::filesystem::path output_file = input_file.parent_path() /
                                        (input_file.stem().string() + "_adj_c" + std::to_string(alpha) +
                                         "_b" + std::to_string(beta) + "." + input_ext);

    std::string vf_filter = "eq=contrast=" + std::to_string(alpha) + ":brightness=" + std::to_string(beta);
    std::string cmd = "ffmpeg -hide_banner -loglevel error -y -i \"" + input_file.string() +
                      "\" -vf \"" + vf_filter + "\" -c:a copy \"" + output_file.string() + "\"";

    int ret = std::system(cmd.c_str());
    if (ret != 0) {
        std::cerr << "⚠ Error: FFmpeg failed to adjust video!" << std::endl;
        return 1;
    }

    if (remove_original) {
        try {
            std::filesystem::remove(input_file);
            std::cout << "⚠ Original file " << input_file << " removed after generating " << output_file << std::endl;
        } catch (const std::filesystem::filesystem_error& e) {
            std::cerr << "⚠ Error removing original file: " << e.what() << std::endl;
        }
    }

    std::cout << "Video adjusted (contrast=" << alpha << ", brightness=" << beta << ") → " << output_file << std::endl;
    std::cout << "✓ Adjust complete!" << std::endl;
    return 0;
}