# img-filterer
Simple program in Python that lets you add filters on images. Project made for Python classes at University. It uses:
 - PyQt5
 - ctypes
 - python-pillow 
 ## How it works
It let's you choose image from disk, converts it to greyscale and shows in window. Then, you can provide 3x3 kernel convolution matrix, hit 'Apply filter' and you'll see result of given filter in window. Filters can be chained. You can save result to JPEG as well.

Under the hood it calls functions from custom made DLL (Visual Studio solution) that changes image data by applying given kernel convolution matrix over the image.
## Sample filters
Sobel filter (edge detection):
`[[1, 0, -1], [2, 0, -2], [1, 0, -1]]`

Mean blur:
`[[0.1, 0.1, 0.1], [0.1, 0.1, 0.1], [0.1, 0.1, 0.1]]`

Gaussian blur:
`[[1,2,1], [2,4,2], [1,2,1]]`

## Sample images
In folder `example_images` you can find some photos in a few resolutions.
