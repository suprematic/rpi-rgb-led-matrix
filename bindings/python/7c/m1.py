from samplebase import SampleBase
from rgbmatrix import graphics
from functools import reduce
import time
import urllib.request
from urllib.error import URLError, HTTPError
from datetime import datetime
import json

# TODO change to the panel's name
PANEL_NAME = "7c-m1-r1"

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

class SevenCourtsM1(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SevenCourtsM1, self).__init__(*args, **kwargs)        

    def run(self):
        self.canvas = self.matrix.CreateFrameCanvas()

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

        panel_id = self.register()
        match = None
        while True:
            self.canvas.Clear()
            try:
                match = match_info(panel_id)
            except URLError as e:
                print(e)
                self.draw_error_indicator()                
            if match != None:
                self.display_match(match)
            else:
                self.display_clock(self.canvas)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            time.sleep(1)

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
        font = self.font_XL
        color = self.color_grey        
        text = datetime.now().strftime('%H:%M:%S')
        graphics.DrawText(canvas, font, 80, 60, color, text)

    def display_match(self, match):
        color = graphics.Color(64, 64, 64)
        color_set = graphics.Color(0, 32, 32)
        color_service = graphics.Color(32, 64, 0)

        name1 = team_name(match["team1"]["name"])
        name2 = team_name(match["team2"]["name"])
        self.draw_text(0, 10, color, name1)
        self.draw_text(0, 30, color, name2)

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
        self.draw_text(game_score1X, 10, color, game_score1)
        self.draw_text(game_score2X, 30, color, game_score2)

        set_scores1 = match["team1"]["setScores"]
        set_scores2 = match["team2"]["setScores"]
        set_scores1_x = 77 - (len(set_scores1) * 8)
        set_scores2_x = 77 - (len(set_scores2) * 8)
        for score in [s for s in set_scores1 if s != None]:
            score = str(score)
            self.draw_text(set_scores1_x, 10, color_set, score)
            set_scores1_x = set_scores1_x + 8
        for score in [s for s in set_scores2 if s != None]:
            score = str(score)
            self.draw_text(set_scores2_x, 30, color_set, score)
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

    def draw_text(self, x, y, color, text):
        return graphics.DrawText(self.canvas, self.font_S, x, y, color, text)

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
