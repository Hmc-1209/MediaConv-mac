#ifndef VIDEO_CONVERTER_H
#define VIDEO_CONVERTER_H

extern "C" {
    int reformat_video(const char* input_path, const char* output_ext, int overwrite);
    int resize_video(const char* input_path, int width, int height, int overwrite);
    void crop_video();
    void rotate_video();
    void flip_video();
    void adjust_brightness_video();
}

#endif
