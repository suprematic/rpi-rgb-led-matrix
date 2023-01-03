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

#BASE_URL = "https://staging.tableau.tennismath.com"
BASE_URL = "http://192.168.114.30:5000"
REGISTRATION_URL = BASE_URL + "/panels/"

# Constants for the 7C M1 panel (P5 192 x 64)
PANEL_WIDTH = 192
PANEL_HEIGHT = 64

def log(*args):
    print(*args, flush=True)    

def match_url(panel_id):
    return BASE_URL + "/panels/" + panel_id + "/match"

def register():
    data = json.dumps({"code": PANEL_NAME}).encode('utf-8')
    url = REGISTRATION_URL
    request = urllib.request.Request(url, data=data, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            j = json.loads(response.read().decode('utf-8'))
            log(url, "registered:", j)
            return j["id"]
    except HTTPError as e:
        log(url, e)
        return None

def match_info(panel_id):
    url = match_url(panel_id)
    with urllib.request.urlopen(url, timeout=10) as response:
        if response.status == 200:
            j = json.loads(response.read().decode('utf-8'))
            log(url, "match:", j)
            return j
        log("url='" + url + "', status= " + str(response.status))
    return None

# Style constants
COLOR_WHITE = graphics.Color(255, 255, 255)
COLOR_GREY = graphics.Color(192, 192, 192)
COLOR_GREY_DARK = graphics.Color(96, 96, 96)
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

COLOR_SCORE_SET = COLOR_GREY
COLOR_SCORE_SET_WON = COLOR_SCORE_SET
COLOR_SCORE_SET_LOST = COLOR_GREY_DARK
COLOR_SCORE_GAME = COLOR_GREY
COLOR_SCORE_SERVICE = COLOR_YELLOW
COLOR_TEAM_NAME = COLOR_GREY
FONT_SCORE = FONT_XL
FONT_TEAM_NAME_S = FONT_S
FONT_TEAM_NAME_M = FONT_M
FONT_TEAM_NAME_L = FONT_L
FONT_TEAM_NAME_XL = FONT_XL

class SevenCourtsM1(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SevenCourtsM1, self).__init__(*args, **kwargs)        

    def run(self):
        self.canvas = self.matrix.CreateFrameCanvas()
        while True:
            panel_id = self.register()
            match = None

            # FIXME fancy exception handling
            try:
                while True:
                    self.canvas.Clear()
                    match = match_info(panel_id)
                    if match != None:
                        self.display_match(match)
                    else:
                        self.display_clock()
                    self.canvas = self.matrix.SwapOnVSync(self.canvas)
                    time.sleep(1)
            except URLError as e:
                log(e)
            except socket.timeout as e:
                log('Socket timeout', e)
            except Exception as e:
                log(e)

    def register(self):
        panel_id = None
        while True:
            self.canvas.Clear()

            # FIXME fancy exception handling
            try:
                panel_id = register()
            except URLError as e:
                log(e)
                self.draw_error_indicator()
            except socket.timeout as e:
                log('Socket timeout', e)
                self.draw_error_indicator()
            except Exception as e:
                log(e)
                self.draw_error_indicator()            

            if panel_id != None:
                return panel_id
            else:
                self.display_clock()
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            time.sleep(1)

    def display_clock(self):
        text = datetime.now().strftime('%H:%M:%S')
        self.draw_text(80, 60, text, FONT_XL, COLOR_GREY)


    def display_score(self, match):

        t1_on_serve=match["team1"]["serves"]
        t2_on_serve=match["team2"]["serves"]
        t1_set_scores = match["team1"]["setScores"]
        t2_set_scores = match["team2"]["setScores"]

        is_match_over = match["matchResult"] != None
        
        if (len(t1_set_scores)=0):
            t1_set1 = t2_set1 = t1_set2 = t2_set2 = t1_set3 = t2_set3 = ""
            c_t1_set1 = c_t2_set1 = c_t1_set2 = c_t2_set2 = c_t1_set3 = c_t2_set3 = COLOR_BLACK
        elif (len(t1_set_scores)=1):
            t1_set1 = match["team1"]["setScores"][0]
            t2_set1 = match["team2"]["setScores"][0]
            t1_set2 = t2_set2 = t1_set3 = t2_set3 = ""
            
            if is_match_over:
                c_t1_set1 = COLOR_SCORE_SET_WON if t1_set1>t2_set1 else COLOR_SCORE_SET_LOST
                c_t2_set1 = COLOR_SCORE_SET_WON if t2_set1>t1_set1 else COLOR_SCORE_SET_LOST
            else
                c_t1_set1 = c_t2_set1 = COLOR_SCORE_SET
            c_t1_set2 = c_t2_set2 = c_t1_set3 = c_t2_set3 = COLOR_BLACK

        elif (len(t1_set_scores)=2):
            t1_set1 = match["team1"]["setScores"][0]
            t2_set1 = match["team2"]["setScores"][0]
            t1_set2 = match["team1"]["setScores"][1]
            t2_set2 = match["team2"]["setScores"][1]
            t1_set3 = t2_set3 = ""
            
            c_t1_set1 = COLOR_SCORE_SET_WON if t1_set1>t2_set1 else COLOR_SCORE_SET_LOST
            c_t2_set1 = COLOR_SCORE_SET_WON if t2_set1>t1_set1 else COLOR_SCORE_SET_LOST
            if is_match_over:
                c_t1_set2 = COLOR_SCORE_SET_WON if t1_set2>t2_set2 else COLOR_SCORE_SET_LOST
                c_t2_set2 = COLOR_SCORE_SET_WON if t2_set2>t1_set2 else COLOR_SCORE_SET_LOST
            else
                c_t1_set2 = c_t2_set2 = COLOR_SCORE_SET
            c_t1_set3 = c_t2_set3 = COLOR_BLACK

        elif (len(t1_set_scores)=3):
            t1_set1 = match["team1"]["setScores"][0]
            t2_set1 = match["team2"]["setScores"][0]
            t1_set2 = match["team1"]["setScores"][1]
            t2_set2 = match["team2"]["setScores"][1]
            t1_set3 = match["team1"]["setScores"][2]
            t2_set3 = match["team2"]["setScores"][2]
            c_t1_set1 = COLOR_SCORE_SET_WON if t1_set1>t2_set1 else COLOR_SCORE_SET_LOST
            c_t2_set1 = COLOR_SCORE_SET_WON if t2_set1>t1_set1 else COLOR_SCORE_SET_LOST
            c_t1_set2 = COLOR_SCORE_SET_WON if t1_set2>t2_set2 else COLOR_SCORE_SET_LOST
            c_t2_set2 = COLOR_SCORE_SET_WON if t2_set2>t1_set2 else COLOR_SCORE_SET_LOST
            if is_match_over:
                c_t1_set3 = COLOR_SCORE_SET_WON if t1_set3>t2_set3 else COLOR_SCORE_SET_LOST
                c_t2_set3 = COLOR_SCORE_SET_WON if t2_set3>t1_set3 else COLOR_SCORE_SET_LOST
            else
                c_t1_set3 = c_t2_set3 = COLOR_SCORE_SET
        else:
            #4+ sets are not supported yet


        t1_game = match["team1"].get("gameScore", "")
        t2_game = match["team2"].get("gameScore", "")
        t1_game = str(t1_game if t1_game != None else "")
        t2_game = str(t2_game if t2_game != None else "")
        
        y_T1 = 26
        y_T2 = 58
        y_service_delta = 13

        x_game = 163
        x_service = 155
        w_set = 20
        x_set1 = 96
        x_set2 = x_set1 + w_set
        x_set3 = x_set2 + w_set        

        graphics.DrawText(self.canvas, FONT_SCORE, x_set1, y_T1, c_t1_set1, str(t1_set1))
        graphics.DrawText(self.canvas, FONT_SCORE, x_set2, y_T1, COLOR_SCORE_SET, str(t1_set2))
        graphics.DrawText(self.canvas, FONT_SCORE, x_set3, y_T1, COLOR_SCORE_SET, str(t1_set3))
        graphics.DrawText(self.canvas, FONT_SCORE, x_game, y_T1, COLOR_SCORE_GAME, str(t1_game))

        graphics.DrawText(self.canvas, FONT_SCORE, x_set1, y_T2, COLOR_SCORE_SET, str(t2_set1))
        graphics.DrawText(self.canvas, FONT_SCORE, x_set2, y_T2, COLOR_SCORE_SET, str(t2_set2))
        graphics.DrawText(self.canvas, FONT_SCORE, x_set3, y_T2, COLOR_SCORE_SET, str(t2_set3))
        graphics.DrawText(self.canvas, FONT_SCORE, x_game, y_T2, COLOR_SCORE_GAME, str(t2_game))

        # FIXME shift set scores
        #set_scores_t1 = match["team1"]["setScores"]
        #set_scores_t2 = match["team2"]["setScores"]
        #set_scores_t1_x = 77 - (len(set_scores_t1) * 8)
        #set_scores_t2_x = 77 - (len(set_scores_t2) * 8)
        #for score in [s for s in set_scores_t1 if s != None]:
        #    score = str(score)
        #    self.draw_text(set_scores_t1_x, 10, score)
        #    set_scores_t1_x = set_scores_t1_x + 8
        #for score in [s for s in set_scores_t2 if s != None]:
        #    score = str(score)
        #    self.draw_text(set_scores_t2_x, 30, score)
        #    set_scores_t2_x = set_scores_t2_x + 8

        
        b = (0, 0 ,0)
        y = (96, 96, 0)
        w = (96, 96, 96)
        ball = [
            [b,y,y,y,b],
            [y,y,y,w,y],
            [y,y,w,y,y],
            [y,w,y,y,y],
            [b,y,y,y,b]]        
        if t1_on_serve:
            self.draw_matrix(ball, x_service, y_T1-y_service_delta)
        elif t2_on_serve:
            self.draw_matrix(ball, x_service, y_T2-y_service_delta)

    def display_names(self, match):
        # flag_width = 18 # so far no flags or colors
        flag_width = 0
        flag_height=12

        if match["isTeamEvent"] or not match["isDoubles"]:
            if match["isTeamEvent"]:
                t1p1 = match["team1"]["name"]
                t2p1 = match["team2"]["name"]
            else:
                t1p1 = match["team1"]["p1"]["lastname"]
                t2p1 = match["team2"]["p1"]["lastname"]
            t1p2 = ""
            t2p2 = ""
        elif match["isDoubles"]:
            t1p1 = match["team1"]["p1"]["lastname"]
            t1p2 = match["team1"]["p2"]["lastname"]
            t2p1 = match["team2"]["p1"]["lastname"]
            t2p2 = match["team2"]["p2"]["lastname"]

        max_name_length = max(len(t1p1), len(t1p2), len(t2p1), len(t2p2))
        if max_name_length > 8:
            font = FONT_TEAM_NAME_S
        elif max_name_length > 6:
            font = FONT_TEAM_NAME_M
        else:
            font = FONT_TEAM_NAME_L

        name_length_limit = 13
        t1p1 = t1p1[:name_length_limit].upper()
        t1p2 = t1p2[:name_length_limit].upper()
        t2p1 = t2p1[:name_length_limit].upper()
        t2p2 = t2p2[:name_length_limit].upper()

        if match["isTeamEvent"] or not match["isDoubles"]:
            y_t1 = 26
            y_t2 = 58
            x = flag_width + 2            
            graphics.DrawText(self.canvas, font, x, y_t1, COLOR_TEAM_NAME, t1p1)
            graphics.DrawText(self.canvas, font, x, y_t2, COLOR_TEAM_NAME, t2p1)
        elif match["isDoubles"]:
            y_t1p1 = 2 + flag_height 
            y_t1p2 = y_t1p1 + 2 + flag_height
            y_t2p1 = y_t1p2 + 18
            y_t2p2 = y_t2p1 + 2 + flag_height
            graphics.DrawText(self.canvas, font, flag_width+2, y_t1p1, COLOR_TEAM_NAME, t1p1)
            graphics.DrawText(self.canvas, font, flag_width+2, y_t1p2, COLOR_TEAM_NAME, t1p2)
            graphics.DrawText(self.canvas, font, flag_width+2, y_t2p1, COLOR_TEAM_NAME, t2p1)
            graphics.DrawText(self.canvas, font, flag_width+2, y_t2p2, COLOR_TEAM_NAME, t2p2)

    def display_winner(self, match):
        # FIXME winner is not displayed
        b = (0, 0 ,0)
        r = (128, 0, 0)
        y = (128, 96, 0)
        w = (96, 64, 0)
        cup = [
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
        match_result = match.get("matchResult", None)
        medal_delta=12
        x_medal=PANEL_WIDTH - 2*medal_delta
        if match_result == "T1_WON":
            self.draw_matrix(cup, x_medal, medal_delta)
        elif match_result == "T2_WON":
            self.draw_matrix(cup, x_medal, PANEL_HEIGHT / 2 + medal_delta)

    def display_match(self, match):
        self.display_names(match)
        self.display_score(match)
        self.display_winner(match)

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
