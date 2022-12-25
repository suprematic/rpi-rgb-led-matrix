#!/usr/bin/env python
# -*- coding: utf-8 -*-
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime
from PIL import Image

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

        canvas.SetImage(Image.open("images/flag-france.png").convert('RGB'), 0*18, 0*12)
        canvas.SetImage(Image.open("images/flag-germany.png").convert('RGB'), 1*18, 1*12)
        canvas.SetImage(Image.open("images/flag-italy.png").convert('RGB'), 2*18, 2*12)
        canvas.SetImage(Image.open("images/flag-portugal.png").convert('RGB'), 3*18, 3*12)
        canvas.SetImage(Image.open("images/flag-spain.png").convert('RGB'), 4*18, 0*12)
        canvas.SetImage(Image.open("images/flag-ukraine.png").convert('RGB'), 0*18, 3*12)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_score_singles_with_flags(self, canvas, duration):
        canvas.Clear()

        y_T1 = 26
        y_T2 = 58

        flag_height = 12
        flag_width = 18

        canvas.SetImage(Image.open("images/flag-switzerland.png").convert('RGB'),   0, 10)
        canvas.SetImage(Image.open("images/flag-spain.png").convert('RGB'),   0, 42)
        
        
        color_name = self.color_grey
        font = graphics.Font()
        font.LoadFont("../fonts/texgyre-27.bdf")

        graphics.DrawText(canvas, font, flag_width+2, y_T1, color_name, "FED")
        graphics.DrawText(canvas, font, flag_width+2, y_T2, color_name, "NAD")
        
        self.render_score_3_sets(canvas)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def render_names_doubles(self, canvas, n1, n2, n3, n4, font_path="../fonts/7x13.bdf"):

        flag_height=12
        flag_width=18

        y_T1P1 = 2 + flag_height 
        y_T1P2 = y_T1P1 + 2 + flag_height
        y_T2P1 = y_T1P2 + 18
        y_T2P2 = y_T2P1 + 2 + flag_height
        
        color_name = self.color_grey
        font = graphics.Font()
        font.LoadFont(font_path)

        graphics.DrawText(canvas, font, flag_width+2, y_T1P1, color_name, n1.upper())
        graphics.DrawText(canvas, font, flag_width+2, y_T1P2, color_name, n2.upper())
        graphics.DrawText(canvas, font, flag_width+2, y_T2P1, color_name, n3.upper())
        graphics.DrawText(canvas, font, flag_width+2, y_T2P2, color_name, n4.upper())


    def show_score_doubles_with_flags_long(self, canvas, duration):
        canvas.Clear()

        flag_height = 12
        flag_width = 18

        canvas.SetImage(Image.open("images/flag-italy.png").convert('RGB'),   0, 3)
        canvas.SetImage(Image.open("images/flag-spain.png").convert('RGB'),   0, 3+flag_height+2)
        canvas.SetImage(Image.open("images/flag-france.png").convert('RGB'),  0, 3+flag_height+2+flag_height+3+3)
        canvas.SetImage(Image.open("images/flag-ukraine.png").convert('RGB'), 0, 3+flag_height+2+flag_height+3+3+flag_height+2)



        self.render_names_doubles(canvas, "Schiavionne", "Berrettini", "Shinkarenko", "Dolgopolov")
        
        self.render_score_3_sets(canvas)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_score_doubles_with_flags_short(self, canvas, duration):
        canvas.Clear()

        flag_height = 12
        flag_width = 18

        canvas.SetImage(Image.open("images/flag-italy.png").convert('RGB'),   0, 6 + 3)
        canvas.SetImage(Image.open("images/flag-spain.png").convert('RGB'),   0, 6 + 3+flag_height+2+flag_height+3+3)        

        # FIXME support accents, umlauts etc (Gonzalez)
        self.render_names_doubles(canvas, "Rossi", "Bianchi", "Gonzalez", "Lopez", "../fonts/9x15.bdf")
        
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

    def show_logos(self, canvas, duration):
        canvas.Clear()

        image = Image.open("images/waldau_generali_transparent.png")
        # image.thumbnail((64*3, 32*2), Image.ANTIALIAS)
        # self.matrix.SetImage(image.convert('RGB'))

        canvas.SetImage(image.convert('RGB'))

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)


    def run_slide_show(self, durationPerScreen):
        
        canvas = self.matrix.CreateFrameCanvas()
        
        self.show_score_doubles_with_flags_short(canvas, durationPerScreen)




        self.show_score_doubles_with_flags_long(canvas, durationPerScreen)

        
        self.show_score_singles_with_flags(canvas, durationPerScreen)


        self.show_logos(canvas, durationPerScreen)
        self.show_clock(canvas, durationPerScreen)

        self.show_flags(canvas, durationPerScreen)
            
        


# Main function
if __name__ == "__main__":
    demo = M1_Demo()
    if (not demo.process()):
        demo.print_help()
    
