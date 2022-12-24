#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from datetime import datetime
from PIL import Image

class M1_Demo(SampleBase):
    def __init__(self, *args, **kwargs):
        super(M1_Demo, self).__init__(*args, **kwargs)
        self.parser.add_argument("-d", "--delay", help="Delay between frames", default=8)
    
        self.clrWhite = graphics.Color(255, 255, 255) 
        self.clrRed = graphics.Color(255, 0, 0) 
        self.clrYellow = graphics.Color(255, 255, 0) 
        self.clrGreen = graphics.Color(0, 255, 0)
        self.clrGrey = graphics.Color(128, 128, 128)

        self.fntXL = graphics.Font()
        self.fntXL.LoadFont("fonts/texgyre-27.bdf")
        


    def run(self):
        delay = int(self.args.delay)
        for x in range(100000):
            self.runSlideShow(delay)

    def showFlags(self, canvas, duration):
        canvas.Clear()

        canvas.SetImage(Image.open("images/flag-france.png").convert('RGB'), 0*18, 0*12)
        canvas.SetImage(Image.open("images/flag-germany.png").convert('RGB'), 1*18, 1*12)
        canvas.SetImage(Image.open("images/flag-italy.png").convert('RGB'), 2*18, 2*12)
        canvas.SetImage(Image.open("images/flag-portugal.png").convert('RGB'), 3*18, 3*12)
        canvas.SetImage(Image.open("images/flag-spain.png").convert('RGB'), 4*18, 0*12)
        canvas.SetImage(Image.open("images/flag-ukraine.png").convert('RGB'), 0*18, 3*12)

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def showScoreDoublesWithFlags(self, canvas, duration):
        canvas.Clear()

        fH = 12
        fW = 18


        canvas.SetImage(Image.open("images/flag-italy.png").convert('RGB'),   0, 2)
        canvas.SetImage(Image.open("images/flag-spain.png").convert('RGB'),   0, 2+fH+2+2)
        canvas.SetImage(Image.open("images/flag-france.png").convert('RGB'),  0, 2+fH+2+2+fH+2+2)
        canvas.SetImage(Image.open("images/flag-ukraine.png").convert('RGB'), 0, 2+fH+2+2+fH+2+2+fH+2+2)
        
        

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def showClock(self, canvas, duration):
        
        clrClock = self.clrGrey

        for x in range(duration):
            canvas.Clear()
            txtClock=datetime.now().strftime('%H:%M:%S')
            graphics.DrawText(canvas, self.fntXL, 80, 60, clrClock, txtClock)
            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(1)

    def showLogos(self, canvas, duration):
        canvas.Clear()

        image = Image.open("images/waldau_generali_transparent.png")
        # image.thumbnail((64*3, 32*2), Image.ANTIALIAS)
        # self.matrix.SetImage(image.convert('RGB'))

        canvas.SetImage(image.convert('RGB'))

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)

    def showScore(self, canvas, duration):
        canvas.Clear()

        clrName = self.clrGrey
        clrScoreSet = clrName
        clrScoreGame = clrScoreSet
        
        ## Flag Switzerland 10x10
        f1l = 10 
        f1h = 10
        f1x = 63
        f1y = 13

        fl = f1l - 1
        fh = f1h - 1
        fx = f1x
        fy = f1y
        clrF1 = graphics.Color(218, 41, 28)
        clrF2 = self.clrWhite
        graphics.DrawLine(canvas, fx, fy, fx+fl, fy, clrF1)
        graphics.DrawLine(canvas, fx, fy+1, fx+fl, fy+1, clrF1)

        graphics.DrawLine(canvas, fx, fy, fx, fy+fh, clrF1)
        graphics.DrawLine(canvas, fx+1, fy, fx+1, fy+fh, clrF1)

        graphics.DrawLine(canvas, fx+fl, fy, fx+fl, fy+fh, clrF1)
        graphics.DrawLine(canvas, fx+fl-1, fy, fx+fl-1, fy+fh, clrF1)
        graphics.DrawLine(canvas, fx, fy+fh, fx+fl, fy+fh, clrF1)
        graphics.DrawLine(canvas, fx, fy+fh-1, fx+fl, fy+fh-1, clrF1)
        
        graphics.DrawLine(canvas, fx + 1, fy + 1, fx + 1, fy + 1, clrF1)
        graphics.DrawLine(canvas, fx + fl - 1, fy + 1, fx + fl - 1, fy + 1, clrF1)
        graphics.DrawLine(canvas, fx + 1, fy + fh - 1, fx + 1, fy + fh - 1, clrF1)
        graphics.DrawLine(canvas, fx + fl - 1, fy + fh - 1, fx + fl - 1, fy + fh - 1, clrF1)

        graphics.DrawLine(canvas, fx+2, fy+2, fx+fl-2, fy+2, clrF1)
        graphics.DrawLine(canvas, fx+2, fy+2+1, fx+fl-2, fy+2+1, clrF1)
        graphics.DrawLine(canvas, fx+2, fy+fh-2, fx+fl-2, fy+fh-2, clrF1)
        graphics.DrawLine(canvas, fx+2, fy+fh-2-1, fx+fl-2, fy+fh-2-1, clrF1)

        graphics.DrawLine(canvas, fx+4, fy+2, fx+4, fy+fh-2, clrF2)
        graphics.DrawLine(canvas, fx+4+1, fy+2, fx+4+1, fy+fh-2, clrF2)
        graphics.DrawLine(canvas, fx+2, fy+4, fx+fl-2, fy+4, clrF2)
        graphics.DrawLine(canvas, fx+2, fy+4+1, fx+fl-2, fy+4+1, clrF2)

       
        ## Flag Spain 12x10
        f2l = 12 
        f2h = 10
        f2x = 62
        f2y = 47 

        fl = f2l - 1
        fh = f2h - 1
        fx = f2x
        fy = f2y
        clrF1 = graphics.Color(170, 21, 27)
        clrF2 = graphics.Color(241, 191, 0)
        
        graphics.DrawLine(canvas, fx, fy, fx+fl, fy, clrF1)
        graphics.DrawLine(canvas, fx, fy+1, fx+fl, fy+1, clrF1)
        graphics.DrawLine(canvas, fx, fy+fh-1, fx+fl, fy+fh-1, clrF1)
        graphics.DrawLine(canvas, fx, fy+fh, fx+fl, fy+fh, clrF1)

        graphics.DrawLine(canvas, fx, fy+2, fx+fl, fy+2, clrF2)
        graphics.DrawLine(canvas, fx, fy+3, fx+fl, fy+3, clrF2)
        graphics.DrawLine(canvas, fx, fy+4, fx+fl, fy+4, clrF2)
        graphics.DrawLine(canvas, fx, fy+5, fx+fl, fy+5, clrF2)
        graphics.DrawLine(canvas, fx, fy+6, fx+fl, fy+6, clrF2)
        graphics.DrawLine(canvas, fx, fy+7, fx+fl, fy+7, clrF2)

        graphics.DrawLine(canvas, fx+3, fy+4, fx+2+1, fy+3, clrF1)
        graphics.DrawLine(canvas, fx+2, fy+4, fx+2+2, fy+4, clrF1)
        graphics.DrawLine(canvas, fx+2, fy+5, fx+2+2, fy+5, clrF1)
        graphics.DrawLine(canvas, fx+2, fy+6, fx+2+2, fy+6, clrF1)

       
        ## Names and score 
        yT1 = 28
        yT2 = 62
        yServiceDelta = 10

        xGame = 158
        xService = 146
        wSet = 24
        xSet1 = 80
        xSet2 = xSet1 + wSet
        xSet3 = xSet2 + wSet
        
        graphics.DrawText(canvas, self.fntXL, 0, yT1, clrName, "FED")
        graphics.DrawText(canvas, self.fntXL, xSet1, yT1, clrScoreSet, "7")
        graphics.DrawText(canvas, self.fntXL, xSet2, yT1, clrScoreSet, "3")
        graphics.DrawText(canvas, self.fntXL, xSet3, yT1, clrScoreSet, "5")
        graphics.DrawText(canvas, self.fntXL, xService, yT1-yServiceDelta, clrScoreSet, ".")
        graphics.DrawText(canvas, self.fntXL, xGame, yT1, clrScoreSet, "30")


        graphics.DrawText(canvas, self.fntXL, 0, yT2, clrName, "NAD")
        graphics.DrawText(canvas, self.fntXL, xSet1, yT2, clrScoreSet, "6")
        graphics.DrawText(canvas, self.fntXL, xSet2, yT2, clrScoreSet, "6")
        graphics.DrawText(canvas, self.fntXL, xSet3, yT2, clrScoreSet, "4")
        graphics.DrawText(canvas, self.fntXL, xService, yT2-yServiceDelta, clrScoreSet, "")
        graphics.DrawText(canvas, self.fntXL, xGame, yT2, clrScoreSet, "15")


        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(duration)


    def runSlideShow(self, durationPerScreen):
        
        canvas = self.matrix.CreateFrameCanvas()
        
        self.showScoreDoublesWithFlags(canvas, durationPerScreen)

        self.showFlags(canvas, durationPerScreen)

        self.showClock(canvas, durationPerScreen)

        self.showLogos(canvas, durationPerScreen)

        self.showScore(canvas, durationPerScreen)
            
        


# Main function
if __name__ == "__main__":
    demo = M1_Demo()
    if (not demo.process()):
        demo.print_help()
    
