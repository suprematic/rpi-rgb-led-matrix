from samplebase import SampleBase
from rgbmatrix import graphics
from functools import reduce
import time
import urllib.request
from urllib.error import URLError, HTTPError
from datetime import datetime
import json
import socket

PANEL_NAME = socket.gethostname()

BASE_URL = "https://staging.tableau.tennismath.com"
REGISTRATION_URL = BASE_URL + "/panels/"

# Constants for the 7C M1 panel (P5 192 x 64)
PANEL_WIDTH = 192
PANEL_HEIGHT = 64

def match_url(panel_id):
    return BASE_URL + "/panels/" + panel_id + "/match"

def register():
    data = json.dumps({"code": PANEL_NAME}).encode('utf-8')
    url = REGISTRATION_URL
    request = urllib.request.Request(url, data=data, method='POST')
    try:
        with urllib.request.urlopen(request) as response:
            j = json.loads(response.read().decode('utf-8'))
            print(url, "registered:", j)
            return j["id"]
    except HTTPError as e:
        print(url, e)
        return None

def match_info(panel_id):
    url = match_url(panel_id)
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                j = json.loads(response.read().decode('utf-8'))
                print(url, "match:", j)
                return j
            print("url='" + url + "', status= " + str(response.status))
    except HTTPError as e:
        print(url, e)
    return None

def team_name(name):
    names = name.split(" ", 2)[0:2]
    if len(names) > 1:
        [n1, n2] = names
        n1 = n1 + " " if len(n1) <= 2 else n1[0:2] + "."
        n2 = n2[0:1]
        return n1 + n2
    else:
        n = name
        return n if len(n) <= 6 else n[0:4] + "."

# Style constants
COLOR_WHITE = graphics.Color(255, 255, 255)
COLOR_GREY = graphics.Color(128, 128, 128)
COLOR_BLACK = graphics.Color(0, 0, 0)
COLOR_RED = graphics.Color(255, 0, 0)
COLOR_YELLOW = graphics.Color(255, 255, 0)
COLOR_GREEN = graphics.Color(0, 255, 0)

FONT_XL = graphics.Font()
FONT_XL.LoadFont("fonts/texgyre-27.bdf")
FONT_L = graphics.Font()
FONT_L.LoadFont("fonts/10x20.bdf")
FONT_M = graphics.Font()
FONT_M.LoadFont("fonts/9x15.bdf")
FONT_S = graphics.Font()
FONT_S.LoadFont("fonts/7x13.bdf")
FONT_XS = graphics.Font()
FONT_XS.LoadFont("fonts/5x8.bdf")
FONT_XXS = graphics.Font()
FONT_XXS.LoadFont("fonts/tom-thumb.bdf")

# Stylesheet
COLOR_DEFAULT = COLOR_GREY
FONT_DEFAULT = FONT_S

class SevenCourtsM1(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SevenCourtsM1, self).__init__(*args, **kwargs)        

    def run(self):
        self.canvas = self.matrix.CreateFrameCanvas()
        while True:
            panel_id = self.register()
            match = None
            try:
                while True:
                    self.canvas.Clear()
                    match = match_info(panel_id)
                    if match != None:
                        self.display_match(match)
                    else:
                        self.display_clock(self.canvas)
                    self.canvas = self.matrix.SwapOnVSync(self.canvas)
                    time.sleep(1)
            except URLError as e:
                print(e)

    def register(self):
        panel_id = None
        while True:
            self.canvas.Clear()
            try:
                panel_id = register()
            except URLError as e:
                print(e)
                self.draw_error_indicator()                
            if panel_id != None:
                return panel_id
            else:
                self.display_clock(self.canvas)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            time.sleep(1)

    def display_clock(self, canvas):
        text = datetime.now().strftime('%H:%M:%S')
        self.draw_text(80, 60, text, FONT_XL, COLOR_GREY)

    def display_match(self, match):
        
        color_set = COLOR_GREY
        color_service = COLOR_YELLOW

        name1 = team_name(match["team1"]["name"])
        name2 = team_name(match["team2"]["name"])
        self.draw_text(0, 10, name1)
        self.draw_text(0, 30, name2)

        b = (0, 0 ,0)
        y = (96, 96, 0)
        w = (96, 96, 96)
        ball = [
            [b,y,y,y,b],
            [y,y,y,w,y],
            [y,y,w,y,y],
            [y,w,y,y,y],
            [b,y,y,y,b]]
        if match.get("match_result", None) == None:
            if match["team1"]["serves"]:
                self.draw_matrix(ball, 76, 3)
            elif match["team2"]["serves"]:
                self.draw_matrix(ball, 76, 23)

        game_score1 = match["team1"].get("gameScore", "")
        game_score2 = match["team2"].get("gameScore", "")
        game_score1 = str(game_score1 if game_score1 != None else "")
        game_score2 = str(game_score2 if game_score2 != None else "")
        game_score1X = 96 - (len(game_score1) * 7)
        game_score2X = 96 - (len(game_score2) * 7)
        self.draw_text(game_score1X, 10, game_score1)
        self.draw_text(game_score2X, 30, game_score2)

        set_scores1 = match["team1"]["setScores"]
        set_scores2 = match["team2"]["setScores"]
        set_scores1_x = 77 - (len(set_scores1) * 8)
        set_scores2_x = 77 - (len(set_scores2) * 8)
        for score in [s for s in set_scores1 if s != None]:
            score = str(score)
            self.draw_text(set_scores1_x, 10, score)
            set_scores1_x = set_scores1_x + 8
        for score in [s for s in set_scores2 if s != None]:
            score = str(score)
            self.draw_text(set_scores2_x, 30, score)
            set_scores2_x = set_scores2_x + 8

        b = (0, 0 ,0)
        r = (128, 0, 0)
        y = (128, 96, 0)
        w = (96, 64, 0)
        winner1 = [
            [b,r,b,b,b,b,b,r,b],
            [r,r,r,b,b,b,r,r,r],
            [b,r,r,b,b,b,r,r,b],
            [b,r,r,r,b,r,r,r,b],
            [b,b,r,r,r,r,r,b,b],
            [b,b,b,y,y,y,b,b,b],
            [b,b,y,y,y,y,y,b,b],
            [b,b,y,y,y,y,y,b,b],
            [b,b,y,y,y,y,y,b,b],
            [b,b,b,y,y,y,b,b,b]]
        winner2 = [
            [b,b,y,y,y,y,y,b,b],
            [w,y,y,y,y,y,y,y,w],
            [w,b,y,y,y,y,y,b,w],
            [w,b,y,y,y,y,y,b,w],
            [b,w,y,y,y,y,y,w,b],
            [b,b,w,y,y,y,w,b,b],
            [b,b,b,y,y,y,b,b,b],
            [b,b,b,b,y,b,b,b,b],
            [b,b,y,y,y,y,y,b,b],
            [b,b,y,y,y,y,y,b,b]]
        match_result = match.get("match_result", None)
        if match_result == "T1_WON":
            self.draw_matrix(winner1, 80, 2)
        elif match_result == "T2_WON":
            self.draw_matrix(winner1, 80, 20)

    def draw_error_indicator(self):
        b = (0, 0, 0)
        r = (255, 0, 0)
        red_dot = [
            [b,r,r,b],
            [r,r,r,r],
            [r,r,r,r],
            [b,r,r,b]]
        self.draw_matrix(red_dot, PANEL_WIDTH - 4, PANEL_HEIGHT - 4)

    def draw_text(self, x, y, text, font=FONT_DEFAULT, color=COLOR_DEFAULT):
        return graphics.DrawText(self.canvas, font, x, y, color, text)

    def draw_matrix(self, m, x0, y0):
        y = y0
        for row in m:
            x = x0
            for px in row:
                (r, g, b) = px
                self.canvas.SetPixel(x, y, r, g, b)
                x = x + 1
            y = y + 1

# Main function
if __name__ == "__main__":
    infoboard = SevenCourtsM1()
    if (not infoboard.process()):
        infoboard.print_help()
