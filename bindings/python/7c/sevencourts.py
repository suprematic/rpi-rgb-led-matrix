# -----------------------------------------------------------------------------
# Uncomment to use with real SDK https://github.com/hzeller/rpi-rgb-led-matrix
#from rgbmatrix import graphics
# Uncomment to use with emulator https://github.com/ty-porter/RGBMatrixEmulator
from RGBMatrixEmulator import graphics
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

def load_font(path):
    result = graphics.Font()
    result.LoadFont(path)
    return result

# Initial fonts - all from SDK
FONTS_V0 = [
    load_font("fonts/texgyre-27.bdf"),
    load_font("fonts/10x20.bdf"),
    load_font("fonts/9x15.bdf"),
    load_font("fonts/7x13.bdf"),
    load_font("fonts/5x8.bdf"),
    load_font("fonts/tom-thumb.bdf")]

# Spleen fonts
FONTS_V1 = [
    load_font("fonts/spleen-16x32.bdf"),
    load_font("fonts/spleen-12x24.bdf"),
    load_font("fonts/spleen-8x16.bdf"),
    load_font("fonts/spleen-6x12.bdf"),
    load_font("fonts/spleen-5x8.bdf"),
    load_font("fonts/tom-thumb.bdf")]

# Spleen with a compromise L font
FONTS_V2 = [
    load_font("fonts/spleen-16x32.bdf"),
    load_font("fonts/10x20.bdf"),
    load_font("fonts/spleen-8x16.bdf"),
    load_font("fonts/spleen-6x12.bdf"),
    load_font("fonts/spleen-5x8.bdf"),
    load_font("fonts/tom-thumb.bdf")]

FONTS = FONTS_V1

FONT_XL=FONTS[0]
FONT_L=FONTS[1]
FONT_M=FONTS[2]
FONT_S=FONTS[3]
FONT_XS=FONTS[4]
FONT_XXS=FONTS[5]

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

Y_FONT_SYMBOL_NORMAL_HEIGHTS = {
    FONTS_V0[0] : 20,
    FONTS_V0[1] : 13,
    FONTS_V0[2] : 10,
    FONTS_V0[3] : 9,
    FONTS_V0[4] : 6,
    FONTS_V0[5] : 5,

    FONTS_V1[0] : 20,
    FONTS_V1[1] : 15,
    FONTS_V1[2] : 10,
    FONTS_V1[3] : 8,
    FONTS_V1[4] : 6,
    FONTS_V1[5] : 5,

    FONTS_V2[0] : 20,
    FONTS_V2[1] : 13,
    FONTS_V2[2] : 10,
    FONTS_V2[3] : 8,
    FONTS_V2[4] : 6,
    FONTS_V2[5] : 5
}

def y_font_offset(font):
    ## This works only on emulator
    # return Y_FONT_EXTRA_OFFSETS.get(font.headers['fontname'], 0) + font.baseline + font.headers['fbbyoff']
    return Y_FONT_SYMBOL_NORMAL_HEIGHTS.get(font)

def y_font_center(font, container_height):
    """Returns y position for the font to be placed vertically centered"""
    y_offset_font = y_font_offset(font)
    return (container_height - y_offset_font ) / 2 + y_offset_font

def width_in_pixels(font, text):
    result = 0;
    for c in text:
        result+=font.CharacterWidth(ord(c))
    #print('<{}> => {}'.format(text,result))
    return result

def font_fits(font, width, height, *texts):
    
    font_symbol_height = y_font_offset(font)
    max_width_with_this_font = max(map(partial(width_in_pixels, font), *texts))
    #print('{}>={} {}>={} {}'.format(
    #    height, font_symbol_height, width, max_width_with_this_font, *texts))

    result = (height >= font_symbol_height) & (width >= max_width_with_this_font)
    return result

def pick_font_that_fits(width, height, *texts):
    #print('Available container: {}x{}'.format(width, height))
    if font_fits(FONT_XL, width, height, texts):
        result = FONT_XL
    elif font_fits(FONT_L, width, height, texts):
        result = FONT_L
    elif font_fits(FONT_M, width, height, texts):
        result = FONT_M
    else:
        result = FONT_S
    
    debug_font_info(FONT_XL, 'XL')
    debug_font_info(FONT_L, 'L')
    debug_font_info(FONT_M, 'M')
    debug_font_info(FONT_S, 'S')
    debug_font_info(result, "RES")
    return result

def debug_font_info(font, name=''):
    print('Font {} h={} bl={} y_off={}'.format(
        name,
        font.height, 
        font.baseline,
        y_font_offset(font)))


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

def draw_grid(canvas, rows=4, cols=4, color=COLOR_GREY_DARKEST):
    x_step_size = int (PANEL_WIDTH / cols)
    for i in range(cols):
        x = i * x_step_size
        graphics.DrawLine(canvas, x, 0, x, PANEL_HEIGHT, color)
    y_step_size = int (PANEL_HEIGHT / rows)
    for i in range(rows):
        y = i * y_step_size
        graphics.DrawLine(canvas, 0, y, PANEL_WIDTH, y, color)

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