#ifndef IMAGE_CONVERTER_H
#define IMAGE_CONVERTER_H

extern "C" {
    int reformat_image(const char* input_path, const char* output_ext);
    int resize_image(const char* input_path, int width, int height);
    int crop_image(const char* input_path, int start_x, int start_y, int width, int height);
    void rotate_image();
    void flip_image();
    void adjust_brightness_image();
    void batch_process_image();
}

#endif
