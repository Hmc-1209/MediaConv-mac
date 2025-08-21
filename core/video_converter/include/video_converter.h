#ifndef VIDEO_CONVERTER_H
#define VIDEO_CONVERTER_H

extern "C" {
    int reformat_video(const char* input_path, const char* output_ext, int overwrite);
    void resize_video();
    void crop_video();
    void rotate_video();
    void flip_video();
    void adjust_brightness_video();
    void batch_process_video();
}

#endif
