from samplebase import SampleBase
from rgbmatrix import graphics
from functools import reduce
import time
import urllib.request
from urllib.error import URLError, HTTPError
from datetime import datetime
import json

#BASE_URL = "https://app.tennis-math.com"
BASE_URL = "https://staging.tableau.tennismath.com"
#BASE_URL = "http://192.168.114.45:5000"
PANEL_NAME = "7c-m0-r4"
REGISTRATION_URL = BASE_URL + "/panels/"

def matchUrl(panelId):
    return BASE_URL + "/panels/" + panelId + "/match"

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

def matchInfo(panelId):
    url = matchUrl(panelId)
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

def drawMatrix(canvas, m, x0, y0):
    y = y0
    for row in m:
        x = x0
        for px in row:
            (r, g, b) = px
            canvas.SetPixel(x, y, r, g, b)
            x = x + 1
        y = y + 1

def teamName(name):
    names = name.split(" ", 2)[0:2]
    if len(names) > 1:
        [n1, n2] = names
        n1 = n1 + " " if len(n1) <= 2 else n1[0:2] + "."
        n2 = n2[0:1]
        return n1 + n2
    else:
        n = name
        return n if len(n) <= 6 else n[0:4] + "."

class MyText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(MyText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        self.canvas = self.matrix.CreateFrameCanvas()
        self.font = graphics.Font()
        self.font.LoadFont("../../../fonts/7x13B.bdf")
        self.clockFont = graphics.Font()
        self.clockFont.LoadFont("./fonts/5x7.bdf")

        panelId = self.register()
        match = None
        while True:
            self.canvas.Clear()
            try:
                match = matchInfo(panelId)
            except URLError as e:
                print(e)
                b = (0, 0, 0)
                r = (255, 0, 0)
                redDot = [
                    [r,r],
                    [r,r]]
                drawMatrix(self.canvas, redDot, 94, 30)
            if match != None:
                self.displayMatch(match)
            else:
                self.displayTime(self.canvas)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            time.sleep(1)

    def register(self):
        panelId = None
        while True:
            self.canvas.Clear()
            try:
                panelId = register()
            except URLError as e:
                print(e)
                b = (0, 0, 0)
                r = (255, 0, 0)
                redDot = [
                    [r,r],
                    [r,r]]
                drawMatrix(self.canvas, redDot, 94, 30)
            if panelId != None:
                return panelId
            else:
                self.displayTime(self.canvas)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            time.sleep(1)

    def displayTime(self, canvas):
        color = graphics.Color(64, 64, 64)
        text = datetime.now().strftime('%H:%M:%S')
        graphics.DrawText(canvas, self.clockFont, 54, 30, color, text)

    def displayMatch(self, match):
        color = graphics.Color(64, 64, 64)
        setColor = graphics.Color(0, 32, 32)
        servesColor = graphics.Color(32, 64, 0)

        name1 = teamName(match["team1"]["name"])
        name2 = teamName(match["team2"]["name"])
        self.drawText(0, 10, color, name1)
        self.drawText(0, 30, color, name2)

        b = (0, 0 ,0)
        y = (96, 96, 0)
        w = (96, 96, 96)
        ball = [
            [b,y,y,y,b],
            [y,y,y,w,y],
            [y,y,w,y,y],
            [y,w,y,y,y],
            [b,y,y,y,b]]
        if match.get("matchResult", None) == None:
            if match["team1"]["serves"]:
                drawMatrix(self.canvas, ball, 76, 3)
            elif match["team2"]["serves"]:
                drawMatrix(self.canvas, ball, 76, 23)

        gameScore1 = match["team1"].get("gameScore", "")
        gameScore2 = match["team2"].get("gameScore", "")
        gameScore1 = str(gameScore1 if gameScore1 != None else "")
        gameScore2 = str(gameScore2 if gameScore2 != None else "")
        gameScore1X = 96 - (len(gameScore1) * 7)
        gameScore2X = 96 - (len(gameScore2) * 7)
        self.drawText(gameScore1X, 10, color, gameScore1)
        self.drawText(gameScore2X, 30, color, gameScore2)

        setScores1 = match["team1"]["setScores"]
        setScores2 = match["team2"]["setScores"]
        setScore1X = 77 - (len(setScores1) * 8)
        setScore2X = 77 - (len(setScores2) * 8)
        for score in [s for s in setScores1 if s != None]:
            score = str(score)
            self.drawText(setScore1X, 10, setColor, score)
            setScore1X = setScore1X + 8
        for score in [s for s in setScores2 if s != None]:
            score = str(score)
            self.drawText(setScore2X, 30, setColor, score)
            setScore2X = setScore2X + 8

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
        matchResult = match.get("matchResult", None)
        if matchResult == "T1_WON":
            drawMatrix(self.canvas, winner1, 80, 2)
        elif matchResult == "T2_WON":
            drawMatrix(self.canvas, winner1, 80, 20)

    def drawText(self, x, y, color, text):
        return graphics.DrawText(self.canvas, self.font, x, y, color, text)

# Main function
if __name__ == "__main__":
    my_text = MyText()
    if (not my_text.process()):
        my_text.print_help()
