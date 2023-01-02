#!/usr/bin/env python
# -*- coding: utf-8 -*-

from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime
from PIL import Image

# Constants for the 7C M1 panel (P5 192 x 64)
PANEL_WIDTH = 192
PANEL_HEIGHT = 64
CAPTION_DURATION = 3
FRAME_DURATION = 8

class M1_Demo(SampleBase):
    def __init__(self, *args, **kwargs):
        super(M1_Demo, self).__init__(*args, **kwargs)
        self.parser.add_argument("-d", "--duration", help="Duration of each frame, seconds", default=FRAME_DURATION)
        self.parser.add_argument("-t", "--title-duration", help="Duration of title frame, seconds", default=CAPTION_DURATION)

        self.color_white = graphics.Color(255, 255, 255)
        self.color_grey = graphics.Color(128, 128, 128)
        self.color_black = graphics.Color(0, 0, 0)

        self.color_red = graphics.Color(255, 0, 0)
        self.color_yellow = graphics.Color(255, 255, 0)
        self.color_green = graphics.Color(0, 255, 0)

        self.font_XL = graphics.Font()
        self.font_XL.LoadFont("fonts/texgyre-27.bdf")
        self.font_L = graphics.Font()
        self.font_L.LoadFont("fonts/10x20.bdf")
        self.font_M = graphics.Font()
        self.font_M.LoadFont("fonts/9x15.bdf")
        self.font_S = graphics.Font()
        self.font_S.LoadFont("fonts/7x13.bdf")
        self.font_XS = graphics.Font()
        self.font_XS.LoadFont("fonts/5x8.bdf")
        self.font_XXS = graphics.Font()
        self.font_XXS.LoadFont("fonts/tom-thumb.bdf")
        


    def run(self):
        duration = int(self.args.duration)
        caption_duration = int(self.args.title_duration)
        for x in range(100000):
            self.run_slide_show(duration, caption_duration)

    def render_score_3_sets(self, canvas):
        ## pseudo score in 3 sets:
        ## 7-6 3-6 7-4 *30-15

        color_score_set = self.color_grey
        color_score_game = self.color_grey
        
        y_T1 = 26
        y_T2 = 58
        y_service_delta = 10

        x_game = 163
        x_service = 155
        w_set = 20
        x_set1 = 96
        x_set2 = x_set1 + w_set
        x_set3 = x_set2 + w_set
        
        graphics.DrawText(canvas, self.font_XL, x_set1, y_T1, color_score_set, "7")
        graphics.DrawText(canvas, self.font_XL, x_set2, y_T1, color_score_set, "3")
        graphics.DrawText(canvas, self.font_XL, x_set3, y_T1, color_score_set, "5")
        graphics.DrawText(canvas, self.font_XL, x_service, y_T1-y_service_delta, color_score_set, ".")
        graphics.DrawText(canvas, self.font_XL, x_game, y_T1, color_score_set, "30")

        graphics.DrawText(canvas, self.font_XL, x_set1, y_T2, color_score_set, "6")
        graphics.DrawText(canvas, self.font_XL, x_set2, y_T2, color_score_set, "6")
        graphics.DrawText(canvas, self.font_XL, x_set3, y_T2, color_score_set, "4")
        graphics.DrawText(canvas, self.font_XL, x_service, y_T2-y_service_delta, color_score_set, "")
        graphics.DrawText(canvas, self.font_XL, x_game, y_T2, color_score_set, "15")

    def show_flags(self, canvas, duration):
        canvas.Clear()

        canvas.SetImage(Image.open("images/flags/france.png").convert('RGB'), 0*18, 0*12)
        canvas.SetImage(Image.open("images/flags/germany.png").convert('RGB'), 1*18, 1*12)
        canvas.SetImage(Image.open("images/flags/italy.png").convert('RGB'), 2*18, 2*12)
        canvas.SetImage(Image.open("images/flags/portugal.png").convert('RGB'), 3*18, 3*12)
        canvas.SetImage(Image.open("images/flags/spain.png").convert('RGB'), 4*18, 0*12)
        canvas.SetImage(Image.open("images/flags/ukraine.png").convert('RGB'), 0*18, 3*12)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_score_singles_with_flags(self, canvas, duration):
        canvas.Clear()

        y_T1 = 26
        y_T2 = 58

        flag_height = 12
        flag_width = 18

        canvas.SetImage(Image.open("images/flags/switzerland.png").convert('RGB'),   0, 10)
        canvas.SetImage(Image.open("images/flags/spain.png").convert('RGB'),   0, 42)
        
        
        color_name = self.color_grey
        
        graphics.DrawText(canvas, self.font_XL, flag_width+2, y_T1, color_name, "FED")
        graphics.DrawText(canvas, self.font_XL, flag_width+2, y_T2, color_name, "NAD")
        
        self.render_score_3_sets(canvas)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def render_names_doubles(self, canvas, t1p1, t1p2, t2p1, t2p2):

        max_name_length = max(len(t1p1), len(t1p2), len(t2p1), len(t2p2))
        if max_name_length > 8:
            font = self.font_S
        elif max_name_length > 6:
            font = self.font_M
        else:
            font = self.font_L  

        flag_height=12
        flag_width=18

        y_t1p1 = 2 + flag_height 
        y_t1p2 = y_t1p1 + 2 + flag_height
        y_t2p1 = y_t1p2 + 18
        y_t2p2 = y_t2p1 + 2 + flag_height
        
        color_name = self.color_grey
        
        graphics.DrawText(canvas, font, flag_width+2, y_t1p1, color_name, t1p1.upper())
        graphics.DrawText(canvas, font, flag_width+2, y_t1p2, color_name, t1p2.upper())
        graphics.DrawText(canvas, font, flag_width+2, y_t2p1, color_name, t2p1.upper())
        graphics.DrawText(canvas, font, flag_width+2, y_t2p2, color_name, t2p2.upper())


    def show_score_doubles_with_flags_long(self, canvas, duration):
        canvas.Clear()

        flag_height = 12
        flag_width = 18

        canvas.SetImage(Image.open("images/flags/italy.png").convert('RGB'),   0, 3)
        canvas.SetImage(Image.open("images/flags/spain.png").convert('RGB'),   0, 3+flag_height+2)
        canvas.SetImage(Image.open("images/flags/france.png").convert('RGB'),  0, 3+flag_height+2+flag_height+3+3)
        canvas.SetImage(Image.open("images/flags/ukraine.png").convert('RGB'), 0, 3+flag_height+2+flag_height+3+3+flag_height+2)



        self.render_names_doubles(canvas, "Schiavionne", "Berrettini", "Shinkarenko", "Dolgopolov")
        
        self.render_score_3_sets(canvas)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_score_doubles_with_flags_short(self, canvas, duration):
        canvas.Clear()

        flag_height = 12
        flag_width = 18

        canvas.SetImage(Image.open("images/flags/italy.png").convert('RGB'), 0, 6 + 3)
        canvas.SetImage(Image.open("images/flags/spain.png").convert('RGB'), 0, 6 + 3+flag_height+2+flag_height+3+3)

        # FIXME support accents, umlauts etc (Gonzalez)
        self.render_names_doubles(canvas, "Rossi", "Bianchi", "Gonzalez", "Lopez")
        
        self.render_score_3_sets(canvas)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_clock_with_weather_and_announcement(self, canvas, duration):
        canvas.Clear()

        self.render_weather(canvas)
        graphics.DrawText(canvas, self.font_S, 2, 20, self.color_grey, "Happy Wedding Day!")
        graphics.DrawText(canvas, self.font_M, 2, 40, self.color_grey, "John & Mary")
        canvas.SetImage(Image.open("images/clipart/heart_19x16.png").convert('RGB'), 42, 45)
        
        # draw statics also on the swapped canvas before starting clock
        canvas = self.matrix.SwapOnVSync(canvas)

        self.render_weather(canvas)
        graphics.DrawText(canvas, self.font_S, 2, 20, self.color_grey, "Happy Wedding Day!")
        graphics.DrawText(canvas, self.font_M, 2, 40, self.color_grey, "John & Mary")
        canvas.SetImage(Image.open("images/clipart/heart_19x16.png").convert('RGB'), 42, 45)

        self.render_clock(canvas, '%H:%M', 140, 61, 104, 14, self.font_L, duration)


    def render_statics_for_big_clock(self, canvas):
        canvas.Clear()
        image = Image.open("images/logos/sevencourts_152x16.png")
        canvas.SetImage(image.convert('RGB'), (PANEL_WIDTH-image.width)/2, 7)
        canvas = self.matrix.SwapOnVSync(canvas)
        return canvas

    def show_big_clock(self, canvas, duration):
        self.render_statics_for_big_clock(canvas)
        # draw statics also on the swapped canvas before starting clock
        self.render_statics_for_big_clock(canvas)
        self.render_clock(canvas, '%H:%M:%S', 80, 60, 104, 21, self.font_XL, duration)

    def render_statics_for_big_clock_with_weather(self, canvas):
        canvas.Clear()
        self.render_weather(canvas)
        canvas = self.matrix.SwapOnVSync(canvas)
        return canvas

    def show_big_clock_with_weather(self, canvas, duration):
        self.render_statics_for_big_clock_with_weather(canvas)
        # draw statics also on the swapped canvas before starting clock
        self.render_statics_for_big_clock_with_weather(canvas)
        self.render_clock(canvas, '%H:%M:%S', 80, 60, 104, 21, self.font_XL, duration)

    def render_weather(self, canvas):
        x_weather = 134
        y_weather = 2
        image_weather = Image.open("images/weather/sunny_with_clouds_25x20.png").convert('RGB')
        canvas.SetImage(image_weather, x_weather, y_weather)
        graphics.DrawText(
                canvas, 
                self.font_L, 
                x_weather + image_weather.width + 2, 
                y_weather + image_weather.height - 4,
                self.color_grey, 
                '23°')

    def clear_rect(self, canvas, x0, y0, w, h):
        for x in range (x0, x0+w):
            graphics.DrawLine(canvas, x, y0, x, y0+h, self.color_black)

    def render_clock(self, canvas, format, x, y, w, h, font, duration):
        color_clock = self.color_grey
        for _ in range(duration):
            self.clear_rect(canvas, x, y-h, w, h)
            current_time=datetime.now().strftime(format)
            graphics.DrawText(canvas, font, x, y, color_clock, current_time)
            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(1)

    def show_image_centered(self, canvas, path_to_image, duration):
        canvas.Clear()
        image = Image.open(path_to_image).convert('RGB')
        
        # center image
        x = max(0, (PANEL_WIDTH - image.width) / 2)
        y = max(0, (PANEL_HEIGHT - image.height) / 2)        
        
        canvas.SetImage(image, x, y)
        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_title_slide(self, canvas, duration):
        canvas.Clear()

        image = Image.open("images/logos/sevencourts_192x21.png")

        canvas.SetImage(image.convert('RGB'), 0, 20)

        graphics.DrawText(canvas, self.font_XS, 4, 60, self.color_grey, "Interactive infoboards for EVERY club")

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_caption(self, canvas, text, duration):
        canvas.Clear()

        graphics.DrawText(canvas, self.font_S, 4, 32, self.color_yellow, text)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_fonts(self, canvas, duration):
        canvas.Clear()
        phrase = 'Quick brown fox jumps over the lazy dog'
        graphics.DrawText(canvas, self.font_XL, 0, 20, self.color_grey, phrase)
        graphics.DrawText(canvas, self.font_L, 0, 33, self.color_grey, phrase)
        graphics.DrawText(canvas, self.font_M, 0, 44, self.color_grey, phrase)
        graphics.DrawText(canvas, self.font_S, 0, 53, self.color_grey, phrase)
        graphics.DrawText(canvas, self.font_XS, 0, 59, self.color_grey, phrase)
        graphics.DrawText(canvas, self.font_XXS, 0, 64, self.color_grey, phrase)
        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def run_demo_sequence(self, canvas, duration, caption_duration):
        
        # 0. Title slide: SevenCourts logo + slogan
        self.show_title_slide(canvas, duration)


        # 1.1. Idle mode: sequence of logos of our references        
        self.show_caption(canvas, "Club or sponsors logos", caption_duration)
        
        duration_logo = min(2, duration)
        self.show_image_centered(canvas, "images/logos/a-rete_192x51.png", duration_logo)
        self.show_image_centered(canvas, "images/logos/tom-schilke_192x55.png", duration_logo)
        self.show_image_centered(canvas, "images/logos/sv1845_101x64.png", duration_logo)
        

        # 1.2. Idle mode: Clock + Weather + etc.
        self.show_caption(canvas, "Time, weather, etc.", caption_duration)
        self.show_big_clock(canvas, duration)        
        self.show_big_clock_with_weather(canvas, duration)
        self.show_clock_with_weather_and_announcement(canvas, duration)

        # 2.1. Match mode: point-by-point
        self.show_caption(canvas, "Point-by-point score (pro)", caption_duration)
        self.show_score_doubles_with_flags_short(canvas, duration)
        self.show_score_doubles_with_flags_long(canvas, duration)
        self.show_score_singles_with_flags(canvas, duration)


        # 2.2. Match mode: game-by-game
        self.show_caption(canvas, "Game-by-game score", caption_duration)
        #self.show_score_doubles_with_flags_short(canvas, duration)
        #self.show_score_doubles_with_flags_long(canvas, duration)
        #self.show_score_singles_with_flags(canvas, duration)

        self.show_caption(canvas, "Price: M1 999€ / XS 399€", caption_duration)


    def run_slide_show(self, duration, caption_duration):
        canvas = self.matrix.CreateFrameCanvas()

        self.run_demo_sequence(canvas, duration, caption_duration)        

        #self.show_flags(canvas, duration)
        #self.show_fonts(canvas, duration)
            
        


# Main function
if __name__ == "__main__":
    demo = M1_Demo()
    if (not demo.process()):
        demo.print_help()
    
