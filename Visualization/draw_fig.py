from PIL import Image


# draw input/affected
def draw_binary(filename, array, save=0):
    if len(array.shape) == 1:
        x = 20
    else:
        x = 20 * array.shape[1]
    y = 20 * array.shape[0]
    im = Image.new("RGB", (x, y))
    for i in range(x):
        for j in range(y):
            array_x = int(i / 20)
            array_y = int(j / 20)
            if len(array.shape) == 1:
                value = array[array_y]
            else:
                value = array[array_y][array_x]
            if value == 1:
                im.putpixel((i, j), (255, 0, 0))
            else:
                im.putpixel((i, j), (255, 255, 255))
    if save == 0:
        im.show(filename)
    else:
        im.save('fig/' + filename + '.png')


# draw hidden_states
def draw_hidden_states(filename, array, save=0):
    if len(array.shape) == 1:
        x = 20
    else:
        x = 20 * array.shape[1]
    y = 20 * array.shape[0]
    im = Image.new("RGB", (x, y))
    for i in range(x):
        for j in range(y):
            # print i, j
            array_x = int(i / 20)
            array_y = int(j / 20)
            # print array_x, array_y
            if len(array.shape) == 1:
                value = array[array_y]
            else:
                value = array[array_y][array_x]
            if value > 0:
                saturation = int(255 * value)
                im.putpixel((i, j), (255, 255 - saturation, 255 - saturation))
            else:
                saturation = int(-255 * value)
                im.putpixel((i, j), (255 - saturation, 255 - saturation, 255))
        # raw_input()
    if save == 0:
        im.show(filename)
    else:
        im.save('fig/' + filename + '.png')


# draw bi_hidden_states
def draw_bi_hidden_states(filename, array, save=0):
    if len(array.shape) == 1:
        x = 20
    else:
        x = 20 * array.shape[1]
    y = 20 * (array.shape[0] + 1)
    im = Image.new("RGB", (x, y))
    for i in range(x):
        for j in range(y):
            # print i, j
            array_x = int(i / 20)
            array_y = int(j / 20)
            if array_y < array.shape[0] / 2:
                if len(array.shape) == 1:
                    value = array[array_y]
                else:
                    value = array[array_y][array_x]
                if value > 0:
                    saturation = int(255 * value)
                    im.putpixel((i, j), (255, 255 - saturation, 255 - saturation))
                else:
                    saturation = int(-255 * value)
                    im.putpixel((i, j), (255 - saturation, 255 - saturation, 255))
            elif array_y == array.shape[0] / 2:
                im.putpixel((i, j), (0, 0, 0))
            else:
                if len(array.shape) == 1:
                    value = array[array_y - 1]
                else:
                    value = array[array_y - 1][array_x]
                if value > 0:
                    saturation = int(255 * value)
                    im.putpixel((i, j), (255, 255 - saturation, 255 - saturation))
                else:
                    saturation = int(-255 * value)
                    im.putpixel((i, j), (255 - saturation, 255 - saturation, 255))
        # raw_input()
    if save == 0:
        im.show(filename)
    else:
        im.save('fig/' + filename + '.png')
