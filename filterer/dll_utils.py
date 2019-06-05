from ctypes import *
import numpy as np
import math

from filterer.exceptions import *


class Lib:
    def __init__(self, path_to_dll: str):
        self.__LIB_PATH = path_to_dll
        self.__handle = CDLL(self.__LIB_PATH)

    def filter_kernel_conv(self, image: np.ndarray, row_length: np.uint64, kernel: np.ndarray):
        """
        :param image: look down to C++ docs at `image_data`
        :param row_length: width of image in pixels
        :param kernel: look down to C++ docs at `kernel_data`
        :return: None, it changes given image data

        C++ docs:
        /**
         * Applies convolution matrix over given image. Changes given image data
         * It uses toroidal coordinate system on image's edges
         * @param image_data - 1 dimmensional array of 8bit ints representing image in greyscale,
         *  or single channel of image
         * @param pixels_amount - size of an image array, that is the amount of pixels in it
         * @param row_length - number of element in each row on convolution matrix,
         *  required since matrix is passed as flattened 1 dimmensional array
         * @param kernel_data - pointer to convolution matrix;
         *  it should be `kernel_size` x `kernel_size` square matrix,
         *  but passed as flattened 1 dimmensional array
         * @param kernel_size - size of convolution matrix, that is the number of rows
         *  that should be equal to number of columns (known as square matrix :))
         */
        void filter_kernel_conv(uint8_t* image_data, const uint64_t pixels_amount, const uint64_t row_length,
                                const float* kernel_data, const unsigned int kernel_size);
        """

        if kernel.ndim == 2:
            rows, cols = kernel.shape
            if rows != cols:
                raise InvalidKernelConvolutionDataError(
                    "Convolution matrix must be a squere matrix!"
                )
            if rows % 2 == 0:
                raise InvalidKernelConvolutionDataError(
                    "Convolution matrix must be a squere matrix "
                    "with odd number of rows/columns!"
                )
            kernel = kernel.flatten()
            kernel_size = rows
        elif kernel.ndim == 1:
            kernel_size = math.sqrt(kernel.size)
            if not kernel_size.is_integer():
                raise InvalidKernelConvolutionDataError(
                    "Convolution matrix must be a squere matrix!"
                )
            if kernel_size % 2 == 0:
                raise InvalidKernelConvolutionDataError(
                    "Convolution matrix must be a squere matrix "
                    "with odd number of rows/columns!"
                )
            kernel_size = c_int(int(kernel_size))
        else:
            raise InvalidKernelConvolutionDataError(
                "Convolution matrix must be at most 2 dimensional!"
            )

        handler = self.__handle.filter_kernel_conv
        handler.argtypes = (
            np.ctypeslib.ndpointer(np.uint8),
            c_ulonglong,
            c_ulonglong,
            np.ctypeslib.ndpointer(np.float32),
            c_int
        )
        handler.restype = None

        handler(image, image.size, row_length, kernel, kernel_size)
