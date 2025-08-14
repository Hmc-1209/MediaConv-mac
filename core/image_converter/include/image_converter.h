#ifndef IMAGE_CONVERTER_H
#define IMAGE_CONVERTER_H

extern "C" {
    void reformat_image();
    void resize_image();
    void crop_image();
    void rotate_image();
    void flip_image();
    void adjust_brightness_image();
    void batch_process_image();
}

#endif
