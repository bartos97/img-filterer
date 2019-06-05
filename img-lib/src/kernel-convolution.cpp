#include "pch.h"
#include "src/kernel-convolution.h"


void IMGLIB_API filter_kernel_conv(uint8_t* image_data, const uint64_t pixels_amount,
                                   const float* kernel_data, const unsigned int kernel_size)
{
    float some_val = kernel_data[0];
    for (size_t i = 0; i < pixels_amount; i++)
    {
        *image_data *= some_val;
        image_data++;
    }
}
