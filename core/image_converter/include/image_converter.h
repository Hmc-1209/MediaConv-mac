#ifndef IMAGE_CONVERTER_H
#define IMAGE_CONVERTER_H

extern "C" {
    int reformat_image(const char* input_path, const char* output_ext, int overwrite);
    int resize_image(const char* input_path, int width, int height, int overwrite);
    int crop_image(const char* input_path, int start_x, int start_y, int width, int height, int overwrite);
    int rotate_image(const char* input_path, int angle, int overwrite);
    int flip_image(const char* input_path, int direction, int overwrite);
    int adjust_brightness_image(const char* input_path, double alpha, int beta, bool overwrite);
}

#endif
