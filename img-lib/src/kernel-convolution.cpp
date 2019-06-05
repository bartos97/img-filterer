#include "pch.h"
#include "src/kernel-convolution.h"

void IMGLIB_API filter_kernel_conv(int* image_data, const unsigned int pixels_amount, 
                                   const float* kernel_data, const unsigned int kernel_size)
{
    //heap allocated copy of a given image;
    //a) heap becouse image might be quite large
    //b) const copy becouse we'll need original data 
    //  while applying filter that changes given data
    //const int* img_copy = new int[pixels_amount];

    for (size_t i = 0; i < pixels_amount; i++)
    {
        image_data[i] /= 2;
    }

    //delete[] img_copy;
}
