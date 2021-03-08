#!/usr/bin/env python3

import sys
import math
import numpy

import matplotlib.pyplot as plt


def rotate(image: numpy.array, angle: int) -> numpy.array:
    height, width, depth = image.shape
    bpp = depth * 8
    print('image {0}x{1} {2} bpp'.format(width, height, bpp))
    if (depth != 3):
        print('not supported bpp != {0}'.format(3 * 8))
        exit(1)
    x_0 = (height // 2)
    y_0 = (width // 2)
    print('origin x={0} y={1}'.format(x_0, y_0))
    vec_origin = numpy.full(shape=(height * width, 2), fill_value=[x_0, y_0]).T
    vec_pixels = numpy.vstack([
        numpy.mgrid[:height, :width][0].ravel(),
        numpy.mgrid[:height, :width][1].ravel(),
    ]) - vec_origin
    angle = math.radians(-angle)
    R = numpy.array([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), +math.cos(angle)],
    ])
    vec_pixels = numpy.int_(R @ vec_pixels + vec_origin)
    print('generating image ...')   # TODO: optimize O(h*w)
    output = numpy.full(shape=(height, width, 3), fill_value=[0, 0, 0])
    for x in range(height):
        for y in range(width):
            pick_x = vec_pixels.T[y + (x * width)][0]
            pick_y = vec_pixels.T[y + (x * width)][1]
            if 0 <= pick_x < height:
                if 0 <= pick_y < width:
                    output[x][y] = image[pick_x][pick_y]
    return output


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage:\n\x20\x20{sys.argv[0]} <image-path> <angle-ccw>')
        exit(1)
    else:
        image, angle = sys.argv[1], sys.argv[2]
        image = rotate(plt.imread(image), int(angle))
        plt.imshow(image)
        plt.show()
