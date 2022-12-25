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

class M1_Demo(SampleBase):
    def __init__(self, *args, **kwargs):
        super(M1_Demo, self).__init__(*args, **kwargs)
        self.parser.add_argument("-d", "--delay", help="Delay between frames, seconds", default=8)

        self.color_white = graphics.Color(255, 255, 255) 
        self.color_grey = graphics.Color(128, 128, 128)

        self.clr_red = graphics.Color(255, 0, 0) 
        self.clr_yellow = graphics.Color(255, 255, 0) 
        self.clr_green = graphics.Color(0, 255, 0)        

        self.font_XL = graphics.Font()
        self.font_XL.LoadFont("fonts/texgyre-27.bdf")
        self.font_L = graphics.Font()
        self.font_L.LoadFont("../fonts/10x20.bdf") #FIXME
        self.font_M = graphics.Font()
        self.font_M.LoadFont("fonts/9x15.bdf")
        self.font_S = graphics.Font()
        self.font_S.LoadFont("../fonts/5x8.bdf")
        self.font_XS = graphics.Font()
        self.font_XS.LoadFont("../fonts/tom-thumb.bdf") #FIXME
        


    def run(self):
        delay = int(self.args.delay)
        for x in range(100000):
            self.run_slide_show(delay)

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

    def show_clock(self, canvas, duration):
        
        color_clock = self.color_grey

        for x in range(duration):
            canvas.Clear()
            current_time=datetime.now().strftime('%H:%M:%S')
            graphics.DrawText(canvas, self.font_XL, 80, 60, color_clock, current_time)
            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(1)

    def show_logo(self, canvas, path_to_logo, duration):
        canvas.Clear()
        image = Image.open(path_to_logo).convert('RGB')
        
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

        graphics.DrawText(canvas, self.font_S, 4, 60, self.color_grey, "Interactive infoboards for EVERY club")

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_fonts(self, canvas, duration):
        canvas.Clear()

        phrase = 'Quick brown fox jumps over the lazy dog'

        graphics.DrawText(canvas, self.font_XL, 0, 20, self.color_grey, phrase)
        graphics.DrawText(canvas, self.font_L, 5, 34, self.color_grey, phrase)
        graphics.DrawText(canvas, self.font_M, 10, 48, self.color_grey, phrase)
        graphics.DrawText(canvas, self.font_S, 15, 57, self.color_grey, phrase)
        graphics.DrawText(canvas, self.font_XS, 20, 63, self.color_grey, phrase)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)


    def run_slide_show(self, durationPerScreen):
        
        canvas = self.matrix.CreateFrameCanvas()


        self.show_title_slide(canvas, durationPerScreen)

        #self.show_logo(canvas, "images/logos/waldau_64x64.png", durationPerScreen)
        #self.show_logo(canvas, "images/logos/generali_76x61.png", durationPerScreen)
        duration_logo = 2
        self.show_logo(canvas, "images/logos/a-rete_192x51.png", duration_logo)
        self.show_logo(canvas, "images/logos/tom-schilke_192x55.png", duration_logo)
        self.show_logo(canvas, "images/logos/sv1845_101x64.png", duration_logo)
        

        self.show_score_doubles_with_flags_short(canvas, durationPerScreen)




        self.show_score_doubles_with_flags_long(canvas, durationPerScreen)

        
        self.show_score_singles_with_flags(canvas, durationPerScreen)


        
        self.show_clock(canvas, durationPerScreen)

        self.show_flags(canvas, durationPerScreen)
        self.show_fonts(canvas, durationPerScreen)
            
        


# Main function
if __name__ == "__main__":
    demo = M1_Demo()
    if (not demo.process()):
        demo.print_help()
    
