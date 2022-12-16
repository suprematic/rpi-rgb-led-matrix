# Display a simple text
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime
from PIL import Image

def draw_matrix(canvas, m, x0, y0):
    y = y0
    for row in m:
        x = x0
        for px in row:
            (r, g, b) = px
            canvas.SetPixel(x, y, r, g, b)
            x = x + 1
        y = y + 1

def debug(msg):
    print(time.time_ns() / 1000000, msg, flush=True)

def heart(matrix, canvas):
    canvas.Clear()
    r = (218, 41, 28)
    w = (15, 15, 15)
    g = (0, 100, 200)
    heart = [
        [w,w,w,w,w,w,w,w,w,w,g,g,g],
        [w,w,w,w,w,w,w,w,w,w,w,g,g],
        [w,w,w,w,w,w,w,w,w,w,g,w,g],
        [w,w,w,r,r,r,w,r,r,r,w,w,w],
        [w,w,r,r,r,r,r,r,r,r,r,w,w],
        [w,w,r,r,r,r,r,r,r,r,r,w,w],
        [w,w,w,r,r,r,r,r,r,r,w,w,w],
        [w,w,w,w,r,g,r,r,r,w,w,w,w],
        [w,w,w,w,g,r,r,r,w,w,w,w,w],
        [w,w,g,g,w,w,r,w,w,w,w,w,w],
        [w,g,g,g,w,w,w,w,w,w,w,w,w],
        [w,w,g,w,w,w,w,w,w,w,w,w,w],
        [w,w,w,w,w,w,w,w,w,w,w,w,w]]
    draw_matrix(canvas, heart, 5, 6)
    canvas = matrix.SwapOnVSync(canvas)
    time.sleep(500)


class SimpleText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-d", "--delay", help="Delay between frames", default=8)
        
    def run(self):
        debug("init: loading...")
        delay = int(self.args.delay)
        self.canvas = self.matrix.CreateFrameCanvas()
        debug("init: loading fonts...")
        self.font = graphics.Font()
        self.font.LoadFont("./fonts/7x13B.bdf")
        self.clockFont = graphics.Font()
        self.clockFont.LoadFont("./fonts/5x7.bdf")
        debug("init: fonts loaded")
        debug("init: loaded")
        heart(self.matrix, self.canvas)
        #while True:
        #    self.display(delay)
    
    def display(self, delay):
        clrGrey = graphics.Color(128, 128, 128)
        
        ### self.Frame: clock 
        clrClock=clrGrey        

        for x in range(delay):
            debug("clock: clear canvas")
            self.canvas.Clear()
            debug("clock: canvas cleared")
            txtClock=datetime.now().strftime('%H:%M:%S')
            debug("clock: got time")
            graphics.DrawText(self.canvas, self.clockFont, 54, 30, clrClock, txtClock)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            debug("clock: displayed")
            time.sleep(1)

        ### Frame: logos

        image = Image.open("./images/waldau_generali_transparent.png")
        #image.thumbnail((64*3, 32*2), Image.ANTIALIAS)
        image.thumbnail((64 * 1.5, 32 * 1.5), Image.ANTIALIAS)
        self.matrix.SetImage(image.convert('RGB'))

        time.sleep(delay)
        self.canvas.Clear()

        ### Frame: score

        ## Flag Switzerland 10x10

        r = (218, 41, 28)
        w = (255, 255, 255)
        flagSw = [
            [r,r,r,r,r,r,r],
            [r,r,r,w,r,r,r],
            [r,r,r,w,r,r,r],
            [r,w,w,w,w,w,r],
            [r,r,r,w,r,r,r],
            [r,r,r,w,r,r,r],
            [r,r,r,r,r,r,r]]
        draw_matrix(self.canvas, flagSw, 30, 6)

       
        ## Flag Spain 12x10

        r = (255, 10, 0)
        y = (255, 215, 0)
        flagSp = [
            [r,r,r,r,r,r,r],
            [y,y,y,y,y,y,y],
            [y,y,y,y,y,y,y],
            [y,y,y,y,y,y,y],
            [r,r,r,r,r,r,r], ]
        draw_matrix(self.canvas, flagSp, 30, 23)
       
        ## Names and score 

        clrName = clrGrey
        clrScoreSet = clrName
        clrScoreGame = clrScoreSet
        
        yT1 = 28 / 2
        yT2 = 62 / 2
        yServiceDelta = 10 / 2

        xGame = 158 / 2
        xService = 146 / 2
        wSet = 24 / 2
        xSet1 = 80 / 2
        xSet2 = xSet1 + wSet
        xSet3 = xSet2 + wSet
        
        graphics.DrawText(self.canvas, self.font, 0, yT1, clrName, "FED")
        graphics.DrawText(self.canvas, self.font, xSet1, yT1, clrScoreSet, "7")
        graphics.DrawText(self.canvas, self.font, xSet2, yT1, clrScoreSet, "3")
        graphics.DrawText(self.canvas, self.font, xSet3, yT1, clrScoreSet, "5")
        graphics.DrawText(self.canvas, self.font, xService, yT1-yServiceDelta, clrScoreSet, ".")
        graphics.DrawText(self.canvas, self.font, xGame, yT1, clrScoreSet, "30")


        graphics.DrawText(self.canvas, self.font, 0, yT2, clrName, "NAD")
        graphics.DrawText(self.canvas, self.font, xSet1, yT2, clrScoreSet, "6")
        graphics.DrawText(self.canvas, self.font, xSet2, yT2, clrScoreSet, "6")
        graphics.DrawText(self.canvas, self.font, xSet3, yT2, clrScoreSet, "4")
        graphics.DrawText(self.canvas, self.font, xService, yT2-yServiceDelta, clrScoreSet, "")
        graphics.DrawText(self.canvas, self.font, xGame, yT2, clrScoreSet, "15")


        self.canvas = self.matrix.SwapOnVSync(self.canvas)
        time.sleep(delay)

# Main function
if __name__ == "__main__":
    simple_text = SimpleText()
    if (not simple_text.process()):
        simple_text.print_help()
    
