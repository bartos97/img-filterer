#include "pch.h"
#include "src/kernel-convolution.h"


inline uint8_t apply_kernel_bounds_check(const uint64_t& x, const uint64_t& y,
                                         const uint64_t& row_length, const uint64_t& column_length,
                                         const Kernel& kernel, 
                                         uint8_t* img_copy)
{
    int move_in_x, move_in_y;
    uint64_t current_x, current_y, current_point;
    unsigned int current_kernel_point;
    int tmp_sum = 0;

    for (unsigned int kernel_x = 0; kernel_x < kernel.size; kernel_x++)
    {
        for (unsigned int kernel_y = 0; kernel_y < kernel.size; kernel_y++)
        {
            move_in_x = kernel_x - kernel.half_size;
            move_in_y = kernel_y - kernel.half_size;
            current_x = (column_length + x + move_in_x) % column_length;
            current_y = (row_length + y + move_in_y) % row_length;
            current_point = current_x * row_length + current_y;
            current_kernel_point = kernel_x * kernel.size + kernel_y;
            tmp_sum += uint8_t(
                img_copy[current_point] * kernel.data[kernel.last_index - current_kernel_point]
            );
        }
    }

    return uint8_t(tmp_sum);
}


inline uint8_t apply_kernel(const uint64_t& x, const uint64_t& y,
                            const uint64_t& row_length,
                            const Kernel& kernel,
                            uint8_t* img_copy)
{
    int tmp_sum = 0;
    unsigned int kernel_iter = kernel.last_index;

    //iteration over kernel for every pixel
    for (uint64_t xk = x - kernel.half_size; xk <= x + kernel.half_size; xk++)
    {
        for (uint64_t yk = y - kernel.half_size; yk <= y + kernel.half_size; yk++)
        {
            tmp_sum += uint8_t(img_copy[xk * row_length + yk] * kernel.data[kernel_iter]);
            kernel_iter--;
        }
    }

    return uint8_t(tmp_sum);
}


void IMGLIB_API filter_kernel_conv(uint8_t* image_data, const uint64_t pixels_amount, const uint64_t row_length,
                                   const float* kernel_data, const unsigned int kernel_size)
{
    //heap allocated copy of a given image;
    //a) heap becouse image might be quite large (and it's size is determined at runtime)
    //b) copy becouse we'll need original data while applying filter that changes given data
    uint8_t* img_copy = new uint8_t[pixels_amount];
    memcpy(img_copy, image_data, pixels_amount * sizeof(uint8_t));

    const uint64_t column_length = pixels_amount / row_length;

    Kernel kernel = {
        nullptr,
        kernel_size,
        (kernel_size - 1) / 2,
        kernel_size* kernel_size - 1,
        0.0f
    };

    for (size_t i = 0; i <= kernel.last_index; i++)
    {
        kernel.sum += kernel_data[i];
    }

    kernel.data = new float[size_t(kernel.last_index) + 1];
    // normalize kernel convolution matrix if it's necessary
    if (kernel.sum > 1.0f)
    {        
        for (size_t i = 0; i <= kernel.last_index; i++)
        {
            kernel.data[i] = kernel_data[i] / kernel.sum;
        }
    }
    else
    {
        memcpy(kernel.data, kernel_data, sizeof(float) * kernel.size * kernel.size);
    }

    // iterate over pixels where we don't have to worry about getting past the edge
    for (uint64_t x = kernel.half_size; x < column_length - kernel.half_size; x++)
    {
        for (uint64_t y = kernel.half_size; y < row_length - kernel.half_size; y++)
        {
            image_data[x * row_length + y] = apply_kernel(x, y, row_length, kernel, img_copy);
        }
    }

    //now use different method on edges

    //left edge
    for (uint64_t x = 0; x < column_length; x++)
    {
        for (uint64_t y = 0; y < kernel.half_size; y++)
        {
            image_data[x * row_length + y] =
                apply_kernel_bounds_check(x, y, row_length, column_length, kernel, img_copy);
        }
    }

    //right edge
    for (uint64_t x = 0; x < column_length; x++)
    {
        for (uint64_t y = row_length - kernel.half_size; y < row_length; y++)
        {
            image_data[x * row_length + y] = 
                apply_kernel_bounds_check(x, y, row_length, column_length, kernel, img_copy);
        }
    }

    //top edge
    for (uint64_t x = 0; x < kernel.half_size; x++)
    {
        for (uint64_t y = 0; y < row_length; y++)
        {
            image_data[x * row_length + y] =
                apply_kernel_bounds_check(x, y, row_length, column_length, kernel, img_copy);
        }
    }

    //bottom edge
    for (uint64_t x = column_length - kernel.half_size; x < column_length; x++)
    {
        for (uint64_t y = 0; y < row_length; y++)
        {
            image_data[x * row_length + y] =
                apply_kernel_bounds_check(x, y, row_length, column_length, kernel, img_copy);
        }
    }

    delete[] kernel.data;
    delete[] img_copy;
}
