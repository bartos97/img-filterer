#pragma once
#include <cstdint>

#ifdef IMGLIB_EXPORTS
    #define IMGLIB_API __declspec(dllexport)
#else
    #define IMGLIB_API __declspec(dllimport)
#endif // IMGLIB_EXPORTS


/**
 * Applies convolution matrix over given image. Changes given image data
 * It uses toroidal coordinate system on image's edges
 * @param image_data - 1 dimensional array of 8bit ints representing image in greyscale,
 *  or single channel of image
 * @param pixels_amount - size of an image array, that is the amount of pixels in it
 * @param row_length - number of element in each row on convolution matrix, 
 *  required since matrix is passed as flattened 1 dimensional array
 * @param kernel_data - pointer to convolution matrix; 
 *  it should be `kernel_size` x `kernel_size` square matrix, 
 *  but passed as flattened 1 dimensional array
 * @param kernel_size - size of convolution matrix, that is the number of rows
 *  that should be equal to number of columns (known as square matrix :))
 */
extern "C" void IMGLIB_API filter_kernel_conv(uint8_t* image_data, 
                                              const uint64_t pixels_amount, 
                                              const uint64_t row_length,
                                              const float* kernel_data, 
                                              const unsigned int kernel_size);

struct Kernel
{
    float* data;
    unsigned int size;
    unsigned int half_size;
    unsigned int last_index;
    float sum;
};
