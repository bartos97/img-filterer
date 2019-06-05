from ctypes import *
import numpy as np
import math


class Lib:
    def __init__(self, path_to_dll: str):
        self.__LIB_PATH = path_to_dll
        self.__handle = CDLL(self.__LIB_PATH)

    def filter_kernel_conv(self, image: np.ndarray, kernel: np.ndarray):
        """
        :param image: look down to C++ docs at `image_data`
        :param kernel: look down to C++ docs at `kernel_data`
        :return: None, it changes given image data

        C++ docs:
        /**
         * Applies convolution matrix over given image. Changes given image data
         * It uses toroidal coordinate system on image's edges
         * @param image_data - 1 dimmensional array of 8bit ints representing image in greyscale,
         *  or single channel of image
         * @param pixels_amount - size of an image array, that is the amount of pixels in it
         * @param kernel_data - pointer to convolution matrix;
         *  it should be `kernel_size` x `kernel_size` square matrix,
         *  but passed as flattened 1 dimmensional array
         * @param kernel_size - size of convolution matrix, that is the number of rows
         *  that should be equal to number of columns (known as square matrix :))
         */
        void IMGLIB_API filter_kernel_conv(uint8_t* image_data, const uint64_t pixels_amount,
                                           const float* kernel_data, const unsigned int kernel_size);
        """

        handler = self.__handle.filter_kernel_conv
        handler.argtypes = (
            np.ctypeslib.ndpointer(np.uint8),
            c_ulonglong,
            np.ctypeslib.ndpointer(np.float32),
            c_int
        )
        handler.restype = None
        handler(image, image.size, kernel, kernel.size)
