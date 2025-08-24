#ifndef VIDEO_CONVERTER_H
#define VIDEO_CONVERTER_H

extern "C" {
    int reformat_video(const char* input_path, const char* output_ext, int overwrite);
    int resize_video(const char* input_path, int width, int height, int overwrite);
    int crop_video(const char* input_path, int start_x, int start_y, int width, int height, int overwrite);
    int rotate_video(const char* input_path, int angle, int overwrite);
    int flip_video(const char* input_path, int direction, int overwrite);
    int adjust_brightness_video(const char* input_path, double alpha, double beta, bool remove_original);
}

#endif
