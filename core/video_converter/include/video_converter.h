#ifndef VIDEO_CONVERTER_H
#define VIDEO_CONVERTER_H

extern "C" {
    int reformat_video(const char* input_path, const char* output_ext, const char* ffmpeg_path, int overwrite);
    int resize_video(const char* input_path, int width, int height, const char* ffmpeg_path, int overwrite);
    int crop_video(const char* input_path, int start_x, int start_y, int width, int height, const char* ffmpeg_path, int overwrite);
    int rotate_video(const char* input_path, int angle, const char* ffmpeg_path, int overwrite);
    int flip_video(const char* input_path, int direction, const char* ffmpeg_path, int overwrite);
    int adjust_brightness_video(const char* input_path, double alpha, double beta, const char* ffmpeg_path, bool remove_original);
}

#endif
