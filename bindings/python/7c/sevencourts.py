# -----------------------------------------------------------------------------
# Uncomment to use with real SDK https://github.com/hzeller/rpi-rgb-led-matrix
from rgbmatrix import graphics
# Uncomment to use with emulator https://github.com/ty-porter/RGBMatrixEmulator
#from RGBMatrixEmulator import graphics
# -----------------------------------------------------------------------------

from PIL import Image
from functools import partial

# Constants for the 7C M1 panel (P5 192 x 64)
PANEL_WIDTH = 192
PANEL_HEIGHT = 64

FLAG_HEIGHT = 12
FLAG_WIDTH = 18

# Style constants
COLOR_WHITE = graphics.Color(255, 255, 255)
COLOR_GREY = graphics.Color(192, 192, 192)
COLOR_GREY_DARK = graphics.Color(96, 96, 96)
COLOR_GREY_DARKEST = graphics.Color(32, 32, 32)
COLOR_BLACK = graphics.Color(0, 0, 0)
COLOR_RED = graphics.Color(255, 0, 0)
COLOR_YELLOW = graphics.Color(255, 255, 0)
COLOR_GREEN = graphics.Color(0, 255, 0)

COLOR_GREEN_7c = graphics.Color(147, 196, 125)
COLOR_BLUE_7c = graphics.Color(111, 168, 220)
COLOR_GOLD_7c = graphics.Color(255, 215, 0)

COLOR_DEFAULT = COLOR_GREY

FONT_PATHS_V0 = [
    "fonts/texgyre-27.bdf",
    "fonts/10x20.bdf",
    "fonts/9x15.bdf",
    "fonts/7x13.bdf",
    "fonts/5x8.bdf",
    "fonts/tom-thumb.bdf"]

FONT_PATHS_V1 = [
    "fonts/spleen-16x32.bdf",
    "fonts/spleen-12x24.bdf",
    "fonts/spleen-8x16.bdf",
    "fonts/spleen-6x12.bdf",
    "fonts/spleen-5x8.bdf",
    "fonts/tom-thumb.bdf"]

FONT_PATHS = FONT_PATHS_V1

FONT_XL = graphics.Font()
FONT_XL.LoadFont(FONT_PATHS[0])
FONT_L = graphics.Font()
FONT_L.LoadFont(FONT_PATHS[1])
FONT_M = graphics.Font()
FONT_M.LoadFont(FONT_PATHS[2])
FONT_S = graphics.Font()
FONT_S.LoadFont(FONT_PATHS[3])
FONT_XS = graphics.Font()
FONT_XS.LoadFont(FONT_PATHS[4])
FONT_XXS = graphics.Font()
FONT_XXS.LoadFont(FONT_PATHS[5])

FONT_DEFAULT = FONT_S

Y_FONT_EXTRA_OFFSETS = {
    '-misc-spleen-medium-r-normal--32-320-72-72-C-160-ISO10646-1' : 0,
    '-misc-spleen-medium-r-normal--24-240-72-72-C-120-ISO10646-1' : 1,
    '-misc-spleen-medium-r-normal--16-160-72-72-C-80-ISO10646-1' : 2,
    '-misc-spleen-medium-r-normal--12-120-72-72-C-60-ISO10646-1' : 2,
    '-misc-spleen-medium-r-normal--8-80-72-72-C-50-ISO10646-1' : 0,
    '-Raccoon-Fixed4x6-Medium-R-Normal--6-60-75-75-P-40-ISO10646-1' : 1,
    '-Misc-Fixed-Medium-R-Normal--8-80-75-75-C-50-ISO10646-1' : 0,
    '-Misc-Fixed-Medium-R-Normal--13-120-75-75-C-70-ISO10646-1' : 0,
    '-Misc-Fixed-Medium-R-Normal--15-140-75-75-C-90-ISO10646-1' : 1,
    '-Misc-Fixed-Medium-R-Normal--20-200-75-75-C-100-ISO10646-1' : 1,
    '-FreeType-TeX Gyre Adventor-Medium-R-Normal--27-270-72-72-P-151-ISO10646-1' : 1
}

Y_FONT_OFFSETS = {
    '-misc-spleen-medium-r-normal--32-320-72-72-C-160-ISO10646-1' : 20,
    '-misc-spleen-medium-r-normal--24-240-72-72-C-120-ISO10646-1' : 15,
    '-misc-spleen-medium-r-normal--16-160-72-72-C-80-ISO10646-1' : 10,
    '-misc-spleen-medium-r-normal--12-120-72-72-C-60-ISO10646-1' : 8,
    '-misc-spleen-medium-r-normal--8-80-72-72-C-50-ISO10646-1' : 6,
    '-Raccoon-Fixed4x6-Medium-R-Normal--6-60-75-75-P-40-ISO10646-1' : 5,
    '-Misc-Fixed-Medium-R-Normal--8-80-75-75-C-50-ISO10646-1' : 0,
    '-Misc-Fixed-Medium-R-Normal--13-120-75-75-C-70-ISO10646-1' : 0,
    '-Misc-Fixed-Medium-R-Normal--15-140-75-75-C-90-ISO10646-1' : 1,
    '-Misc-Fixed-Medium-R-Normal--20-200-75-75-C-100-ISO10646-1' : 1,
    '-FreeType-TeX Gyre Adventor-Medium-R-Normal--27-270-72-72-P-151-ISO10646-1' : 1
}


def y_font_offset(font):
    print(str(font))
    print(vars(font))
    #return 0
    return Y_FONT_EXTRA_OFFSETS.get(font.headers['fontname'], 0) + font.baseline + font.headers['fbbyoff']

def width_in_pixels(font, text):
    result = 0;
    for c in text:
        result+=font.CharacterWidth(ord(c))
    print('<{}> => {}'.format(text,result))
    return result

def pick_font_that_fits(width, *names):
    print('Available width: {}'.format(width))
    if width > max(map(partial(width_in_pixels, FONT_XL),names)):
        return FONT_XL
    elif width > max(map(partial(width_in_pixels, FONT_L),names)):
        return FONT_L
    elif width > max(map(partial(width_in_pixels, FONT_M),names)):
        return FONT_M
    else:
        return FONT_S


def load_flag_image(flag):
    try:
        return Image.open("images/flags/" + flag + ".png").convert('RGB')
    except Exception as e:
        log(e)
        return Image.open("images/flags/VOID.png").convert('RGB')

def log(*args):
    print(*args, flush=True)


def draw_text(canvas, x, y, text, font=FONT_DEFAULT, color=COLOR_DEFAULT):
    return graphics.DrawText(canvas, font, x, y, color, text)

def draw_matrix(canvas, m, x0, y0):
    y = y0
    for row in m:
        x = x0
        for px in row:
            (r, g, b) = px
            canvas.SetPixel(x, y, r, g, b)
            x = x + 1
        y = y + 1

def fill_rect(canvas, x0: int, y0: int, w: int, h: int, color):
    for x in range (x0, x0+w):
        graphics.DrawLine(canvas, x, y0, x, y0+h, color)