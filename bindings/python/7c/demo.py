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

FLAG_HEIGHT = 12
FLAG_WIDTH = 18

# Style constants
COLOR_WHITE = graphics.Color(255, 255, 255)
COLOR_GREY = graphics.Color(192, 192, 192)
COLOR_GREY_DARK = graphics.Color(96, 96, 96)
COLOR_BLACK = graphics.Color(0, 0, 0)
COLOR_RED = graphics.Color(255, 0, 0)
COLOR_YELLOW = graphics.Color(255, 255, 0)
COLOR_GREEN = graphics.Color(0, 255, 0)

COLOR_CLASSIC = graphics.Color(227, 253, 93)
COLOR_CLASSIC_DARK = graphics.Color(113, 127, 47)

COLOR_CLASSIC = graphics.Color(0, 177, 64)
COLOR_CLASSIC_DARK = graphics.Color(0, 150, 54)

COLOR_GREEN_7c = graphics.Color(147, 196, 125)
COLOR_BLUE_7c = graphics.Color(111, 168, 220)
COLOR_GOLD_7c = graphics.Color(255, 215, 0)

FONT_XL = graphics.Font()
FONT_XL.LoadFont("fonts/texgyre-27.bdf")
FONT_L = graphics.Font()
FONT_L.LoadFont("fonts/10x20.bdf")
FONT_M = graphics.Font()
FONT_M.LoadFont("fonts/9x15.bdf")
FONT_M_B = graphics.Font()
FONT_M_B.LoadFont("fonts/9x15B.bdf")
FONT_S = graphics.Font()
FONT_S.LoadFont("fonts/7x13.bdf")
FONT_XS = graphics.Font()
FONT_XS.LoadFont("fonts/5x8.bdf")
FONT_XXS = graphics.Font()
FONT_XXS.LoadFont("fonts/tom-thumb.bdf")

# Timing defaults
TITLE_DURATION = 3
FRAME_DURATION = 8

class M1_Demo(SampleBase):
    def __init__(self, *args, **kwargs):
        super(M1_Demo, self).__init__(*args, **kwargs)
        self.parser.add_argument("-d", "--duration", help="Duration of each frame, seconds", default=FRAME_DURATION)
        self.parser.add_argument("-t", "--title-duration", help="Duration of title frame, seconds", default=TITLE_DURATION)


    def run(self):
        duration = int(self.args.duration)
        title_duration = int(self.args.title_duration)
        for x in range(100000):
            self.run_slide_show(duration, title_duration)

    def draw_matrix(self, canvas, m, x0, y0):
        y = y0
        for row in m:
            x = x0
            for px in row:
                (r, g, b) = px
                canvas.SetPixel(x, y, r, g, b)
                x = x + 1
            y = y + 1

    def render_score_3_sets(self, canvas, show_game_score, custom_style=False):
        ## pseudo score in 3 sets:
        ## 7-6 3-6 7-4 *30-15

        color_score_set = COLOR_CLASSIC if custom_style else COLOR_GREY
        color_score_set_won = COLOR_CLASSIC if custom_style else COLOR_GREY
        color_score_set_lost = COLOR_CLASSIC_DARK if custom_style else COLOR_GREY_DARK
        color_score_game = COLOR_CLASSIC if custom_style else COLOR_GREY
        
        y_T1 = 26
        y_T2 = 58
        y_service_delta = 14
        x_game = 163
        x_service = 155

        if show_game_score:
            #graphics.DrawText(canvas, FONT_XL, x_service, y_T2-y_service_delta, color_score_set, "")
            graphics.DrawText(canvas, FONT_XL, x_game, y_T2, color_score_set, "15")
            #graphics.DrawText(canvas, FONT_XL, x_service, y_T1-y_service_delta, color_score_set, ".")
            graphics.DrawText(canvas, FONT_XL, x_game, y_T1, color_score_set, "30")

            b = (0, 0 ,0)            
            w = (color_score_game.red, color_score_game.green, color_score_game.blue)
            if custom_style:
                ball = [
                    [b,b,w,b,b],
                    [w,b,w,b,w],
                    [b,w,w,w,b],
                    [w,w,w,w,w],
                    [b,w,w,w,b],
                    [w,b,w,b,w],
                    [b,b,w,b,b]]
            else:
                ball = [
                    [b,b,b,b,b],
                    [b,b,w,b,b],
                    [b,w,w,w,b],
                    [w,w,b,w,w],
                    [b,w,w,w,b],
                    [b,b,w,b,b],
                    [b,b,b,b,b]]
        
            self.draw_matrix(canvas, ball, x_service, y_T1-y_service_delta)

            x_service_and_game_delta = 0
        else:
            x_service_and_game_delta = PANEL_WIDTH - x_service            

        w_set = 20
        x_set1 = 96 + x_service_and_game_delta
        x_set2 = x_set1 + w_set
        x_set3 = x_set2 + w_set
        
        graphics.DrawText(canvas, FONT_XL, x_set1, y_T1, color_score_set_won, "7")
        graphics.DrawText(canvas, FONT_XL, x_set2, y_T1, color_score_set_lost, "3")
        graphics.DrawText(canvas, FONT_XL, x_set3, y_T1, color_score_set, "5")        

        graphics.DrawText(canvas, FONT_XL, x_set1, y_T2, color_score_set_lost, "6")
        graphics.DrawText(canvas, FONT_XL, x_set2, y_T2, color_score_set_won, "6")
        graphics.DrawText(canvas, FONT_XL, x_set3, y_T2, color_score_set, "4")

        

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

    def show_score_singles_with_flags(self, canvas, show_game_score, duration):
        canvas.Clear()

        y_T1 = 26
        y_T2 = 58

        canvas.SetImage(Image.open("images/flags/switzerland.png").convert('RGB'),   0, 10)
        canvas.SetImage(Image.open("images/flags/spain.png").convert('RGB'),   0, 42)
        
        
        color_name = COLOR_GREY

        flag_margin_r = 2
        
        graphics.DrawText(canvas, FONT_XL, FLAG_WIDTH+flag_margin_r, y_T1, color_name, "FED")
        graphics.DrawText(canvas, FONT_XL, FLAG_WIDTH+flag_margin_r, y_T2, color_name, "NAD")
        
        self.render_score_3_sets(canvas, show_game_score)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def render_names_doubles(self, canvas, t1p1, t1p2, t2p1, t2p2, custom_style=False):

        max_name_length = max(len(t1p1), len(t1p2), len(t2p1), len(t2p2))
        if max_name_length > 10:
            font = FONT_S
            flag_margin_r = 1
        elif max_name_length > 8:
            font = FONT_S
            flag_margin_r = 2
        elif max_name_length > 6:
            font = FONT_M_B if custom_style else FONT_M
            flag_margin_r = 2
        else:
            font = FONT_L
            flag_margin_r = 2

        y_t1p1 = 2 + FLAG_HEIGHT 
        y_t1p2 = y_t1p1 + 2 + FLAG_HEIGHT
        y_t2p1 = y_t1p2 + 18
        y_t2p2 = y_t2p1 + 2 + FLAG_HEIGHT
        
        color_name = COLOR_CLASSIC if custom_style else COLOR_GREY
        
        graphics.DrawText(canvas, font, FLAG_WIDTH+flag_margin_r, y_t1p1, color_name, t1p1.upper())
        graphics.DrawText(canvas, font, FLAG_WIDTH+flag_margin_r, y_t1p2, color_name, t1p2.upper())
        graphics.DrawText(canvas, font, FLAG_WIDTH+flag_margin_r, y_t2p1, color_name, t2p1.upper())
        graphics.DrawText(canvas, font, FLAG_WIDTH+flag_margin_r, y_t2p2, color_name, t2p2.upper())


    def show_score_doubles_with_flags_long(self, canvas, show_game_score, duration):
        canvas.Clear()

        canvas.SetImage(Image.open("images/flags/italy.png").convert('RGB'),   0, 3)
        canvas.SetImage(Image.open("images/flags/spain.png").convert('RGB'),   0, 3+FLAG_HEIGHT+2)
        canvas.SetImage(Image.open("images/flags/france.png").convert('RGB'),  0, 3+FLAG_HEIGHT+2+FLAG_HEIGHT+3+3)
        canvas.SetImage(Image.open("images/flags/ukraine.png").convert('RGB'), 0, 3+FLAG_HEIGHT+2+FLAG_HEIGHT+3+3+FLAG_HEIGHT+2)

        self.render_names_doubles(canvas, "Bianchi", "Rodríguez", "Lavigne", "Shinkarenko")
        
        self.render_score_3_sets(canvas, show_game_score)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_score_doubles_with_flags_short(self, canvas, show_game_score, duration, custom_style=False):
        canvas.Clear()

        canvas.SetImage(Image.open("images/flags/italy.png").convert('RGB'), 0, 6 + 3)
        canvas.SetImage(Image.open("images/flags/spain.png").convert('RGB'), 0, 6 + 3+FLAG_HEIGHT+2+FLAG_HEIGHT+3+3)

        # FIXME support accents, umlauts etc (Gonzalez)
        self.render_names_doubles(canvas, "Rossi", "Bianchi", "González", "López", custom_style)
        
        self.render_score_3_sets(canvas, show_game_score, custom_style)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def render_statics_for_announcement(self, canvas, text):
        canvas.Clear()
        self.render_weather(canvas)
        lines = text.split('\n')
        graphics.DrawText(canvas, FONT_S, 2, 20, COLOR_GREY, lines[0])
        graphics.DrawText(canvas, FONT_M, 2, 40, COLOR_GREY, lines[1])
        canvas.SetImage(Image.open("images/clipart/heart_19x16.png").convert('RGB'), 42, 45)
        canvas = self.matrix.SwapOnVSync(canvas)
        return canvas

    def show_clock_with_weather_and_announcement(self, canvas, text, duration):
        self.render_statics_for_announcement(canvas, text)        
        # draw statics also on the swapped canvas before starting clock
        self.render_statics_for_announcement(canvas, text)
        self.render_clock(canvas, '%H:%M', 140, 61, 104, 14, FONT_L, duration)

    def render_statics_for_sponsor_logo(self, canvas, image_path):
        canvas.Clear()        
        image = Image.open(image_path).convert('RGB')
        canvas.SetImage(image, 0, 0)        
        canvas = self.matrix.SwapOnVSync(canvas)
        return canvas

    def show_clock_with_sponsor_logo(self, canvas, image_path, duration):
        self.render_statics_for_sponsor_logo(canvas, image_path)        
        # draw statics also on the swapped canvas before starting clock
        self.render_statics_for_sponsor_logo(canvas, image_path)
        self.render_clock(canvas, '%H:%M:%S', 80, 60, 104, 21, FONT_XL, duration)        
    
    def show_big_clock(self, canvas, duration):
        canvas.Clear()
        self.render_clock(canvas, '%H:%M:%S', 80, 60, 104, 21, FONT_XL, duration)

    def render_statics_for_big_clock_with_weather(self, canvas):
        canvas.Clear()
        self.render_weather(canvas)
        canvas = self.matrix.SwapOnVSync(canvas)
        return canvas

    def show_big_clock_with_weather(self, canvas, duration):
        self.render_statics_for_big_clock_with_weather(canvas)
        # draw statics also on the swapped canvas before starting clock
        self.render_statics_for_big_clock_with_weather(canvas)
        self.render_clock(canvas, '%H:%M:%S', 80, 60, 104, 21, FONT_XL, duration)

    def render_weather(self, canvas):
        x_weather = 134
        y_weather = 2
        image_weather = Image.open("images/weather/sunny_with_clouds_25x20.png").convert('RGB')
        canvas.SetImage(image_weather, x_weather, y_weather)
        graphics.DrawText(
                canvas, 
                FONT_L, 
                x_weather + image_weather.width + 2, 
                y_weather + image_weather.height - 4,
                COLOR_GREY, 
                '23°')

    def clear_rect(self, canvas, x0, y0, w, h):
        for x in range (x0, x0+w):
            graphics.DrawLine(canvas, x, y0, x, y0+h, COLOR_BLACK)

    def render_clock(self, canvas, format, x, y, w, h, font, duration):
        color_clock = COLOR_GREY
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

    def show_title_slide(self, canvas, text, duration):
        canvas.Clear()
        image = Image.open("images/logos/sevencourts_192x21.png")
        canvas.SetImage(image.convert('RGB'), 0, 20)
        graphics.DrawText(canvas, FONT_XS, 4, 60, COLOR_GREY, text)
        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_title_text(self, canvas, text, color, duration):
        canvas.Clear()

        font = FONT_S

        lines = text.split('\n')
        h_total = font.height * len(lines)
        for i in range(len(lines)):
            line = lines[i]
            y = (PANEL_HEIGHT-h_total)/2 + (i+1)*font.height - 2
            line_width = 0
            for c in line:
                line_width+=font.CharacterWidth(ord(c))
            x = (PANEL_WIDTH-line_width)/2            
            graphics.DrawText(canvas, font, x, y, color, line)
        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def show_fonts(self, canvas, duration):
        canvas.Clear()
        phrase = 'Quick brown fox jumps over the lazy dog'
        graphics.DrawText(canvas, FONT_XL, 0, 20, COLOR_GREY, phrase)
        graphics.DrawText(canvas, FONT_L, 0, 33, COLOR_GREY, phrase)
        graphics.DrawText(canvas, FONT_M, 0, 44, COLOR_GREY, phrase)
        graphics.DrawText(canvas, FONT_S, 0, 53, COLOR_GREY, phrase)
        graphics.DrawText(canvas, FONT_XS, 0, 59, COLOR_GREY, phrase)
        graphics.DrawText(canvas, FONT_XXS, 0, 64, COLOR_GREY, phrase)
        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def run_demo_sequence_english(self, canvas, duration, title_duration):
        
        # 0. Title slide: SevenCourts logo + slogan
        self.show_title_slide(canvas, "Interactive infoboards for EVERY club", duration)

        # 1.1. Idle mode: sequence of logos of our references        
        self.show_title_text(canvas, "Sponsor, club,\nor tournament logo", COLOR_GREEN_7c, title_duration)
        
        duration_logo = min(3, duration)
        self.show_image_centered(canvas, "images/logos/a-rete_160x43.png", duration_logo)
        self.show_image_centered(canvas, "images/logos/tom-schilke_192x55.png", duration_logo)
        self.show_image_centered(canvas, "images/logos/sv1845_64x64.png", duration_logo)
        

        # 1.2. Idle mode: Clock + Weather + etc.
        self.show_title_text(canvas, "Time, weather,\npersonal greetings, etc.", COLOR_GREEN_7c, title_duration)
        self.show_big_clock_with_weather(canvas, duration)
        self.show_clock_with_weather_and_announcement(canvas, "Happy Wedding Day!\nJohn & Mary", duration)

        # 2.1. Match mode: point-by-point
        self.show_title_text(canvas, "The Grand Slam moment\nin your club!", COLOR_GREEN_7c, title_duration)
        self.show_score_singles_with_flags(canvas, True, duration)
        self.show_title_text(canvas, "Point-by-point score\n(pro mode)", COLOR_GREEN_7c, title_duration)
        self.show_score_doubles_with_flags_short(canvas, True, duration)
        self.show_score_doubles_with_flags_long(canvas, True, duration)

        # 2.2. Match mode: game-by-game
        self.show_title_text(canvas, "Game-by-game score\n(easy mode)", COLOR_GREEN_7c, title_duration)
        self.show_score_doubles_with_flags_short(canvas, False, duration)

        # 2.3. Match mode: point-by-point custom
        self.show_title_text(canvas, "Customize fonts and colors\nto match your style", COLOR_GREEN_7c, title_duration)
        self.show_score_doubles_with_flags_short(canvas, True, duration, True)

        # 3. Some texts
        self.show_title_text(canvas, "Check the COURT 1\nto see in action", COLOR_BLUE_7c, duration)
        self.show_title_text(canvas, "API for integration with\nany scoring, tournament,\nor back-office system", COLOR_GREEN_7c, title_duration)
        self.show_title_text(canvas, "Web & Video\nlive broadcasting", COLOR_BLUE_7c, title_duration)
        self.show_title_text(canvas, "Operate via mobile app\nor a Bluetooth button", COLOR_GREEN_7c, title_duration)
        self.show_title_text(canvas, "SPECIAL PadelTrend PRICE\n\nXS1 399€    M1 999€\n\nAny other size: on request", COLOR_GOLD_7c, duration)

    def run_demo_sequence_italian(self, canvas, duration, title_duration):
        
        # 0. Title slide: SevenCourts logo + slogan
        self.show_title_slide(canvas, "Tabelloni informativi per OGNI club", duration)

        # 1.1. Idle mode: sequence of logos of our references        
        self.show_title_text(canvas, "Logo dello sponsor,\ndel club o del torneo", COLOR_GREEN_7c, title_duration)
        
        duration_logo = min(3, duration)
        self.show_image_centered(canvas, "images/logos/a-rete_160x43.png", duration_logo)
        self.show_image_centered(canvas, "images/logos/tom-schilke_192x55.png", duration_logo)
        self.show_image_centered(canvas, "images/logos/sv1845_64x64.png", duration_logo)
        

        # 1.2. Idle mode: Clock + Weather + etc.
        self.show_title_text(canvas, "Tempo, meteo,\nsaluti personali, ecc.", COLOR_GREEN_7c, title_duration)
        self.show_big_clock_with_weather(canvas, duration)
        self.show_clock_with_weather_and_announcement(canvas, "Evviva gli sposi!\nRomeo e Giulietta", duration)

        # 2.1. Match mode: point-by-point
        self.show_title_text(canvas, "Il momento del Grande Slam\nnel tuo club!", COLOR_GREEN_7c, title_duration)
        self.show_score_singles_with_flags(canvas, True, duration)
        self.show_title_text(canvas, "Punteggio punto per punto\n(modalità Pro)", COLOR_GREEN_7c, title_duration)
        self.show_score_doubles_with_flags_short(canvas, True, duration)
        self.show_score_doubles_with_flags_long(canvas, True, duration)

        # 2.2. Match mode: game-by-game
        self.show_title_text(canvas, "Punteggio game-by-game\n(modalità facile)", COLOR_GREEN_7c, title_duration)
        self.show_score_doubles_with_flags_short(canvas, False, duration)

        # 2.3. Match mode: point-by-point custom
        self.show_title_text(canvas, "Caratteri e colori\npersonalizzabili\nper abbinarsi al tuo stile", COLOR_GREEN_7c, title_duration)
        self.show_score_doubles_with_flags_short(canvas, True, duration, True)

        # 3. Some texts
        self.show_title_text(canvas, "Controlla il CAMPO 1\nper vederlo in azione", COLOR_BLUE_7c, duration)
        self.show_title_text(canvas, "API per l'integrazione\nconqualsiasi sistema\ndi punteggio, torneo,\no back-office", COLOR_GREEN_7c, title_duration)
        self.show_title_text(canvas, "Web e video in diretta", COLOR_BLUE_7c, title_duration)
        self.show_title_text(canvas, "Operare tramite app mobile\no un pulsante Bluetooth", COLOR_GREEN_7c, title_duration)
        self.show_title_text(canvas, "PREZZO SPECIALE PadelTrend\n\nXS1 399€    M1 999€\n\nAltre dimensioni: chiedici", COLOR_GOLD_7c, duration)


    def run_demo_sequence_court_2(self, canvas, duration):
            
        self.show_clock_with_sponsor_logo(canvas, "images/logos/gimpadel_119x32.png", duration)
        self.show_clock_with_sponsor_logo(canvas, "images/logos/italgreen_163x32.png", duration)


    def run_slide_show(self, duration, title_duration):
        canvas = self.matrix.CreateFrameCanvas()

        self.run_demo_sequence_court_2(canvas, duration)

        self.run_demo_sequence_italian(canvas, duration, title_duration)
        self.run_demo_sequence_english(canvas, duration, title_duration)
        

        #self.show_flags(canvas, duration)
        #self.show_fonts(canvas, duration)
            
        


# Main function
if __name__ == "__main__":
    demo = M1_Demo()
    if (not demo.process()):
        demo.print_help()
    
