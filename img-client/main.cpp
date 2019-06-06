#include "kernel-convolution.h"
#include <random>
#include <cstdint>

int main()
{
    const uint64_t PIXEL_AMOUNT = 300 * 200;
    const uint64_t ROW_LENGTH = PIXEL_AMOUNT / 200;
    uint8_t* image = new uint8_t[PIXEL_AMOUNT];

    const unsigned int KERNEL_SIZE = 3;
    float kernel[KERNEL_SIZE * KERNEL_SIZE] = {
        1.0f, 2.0f, 1.0f,
        2.0f, 4.0f, 2.0f,
        1.0f, 2.0f, 1.0f
    };

    for (size_t i = 0; i < PIXEL_AMOUNT; i++)
    {
        image[i] = std::rand() % 255;
    }

    filter_kernel_conv(image, PIXEL_AMOUNT, ROW_LENGTH, kernel, KERNEL_SIZE);

    delete[] image;
    return 0;
}
