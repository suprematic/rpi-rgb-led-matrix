#!/usr/bin/env python
# Display a simple text
from samplebase import SampleBase
from rgbmatrix import graphics
import time


class SimpleText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to display on the RGB LED panel", default="Hello")
        
    def run(self):
        self.display(self.args.text)
    
    def display_score(self, msg):
        print("Displaying tennis score '{0}'".format(msg))

        if (len(msg)>=12):
            p1_set1 = msg[0]
            p1_set2 = msg[1]
            p1_set3 = msg[2]
            p1_serv = msg[3]
            p1_game1 = msg[4]
            p1_game2 = msg[5]
            p2_set1 = msg[6]
            p2_set2 = msg[7]
            p2_set3 = msg[8]
            p2_serv = msg[9]
            p2_game1 = msg[10]
            p2_game2 = msg[11]

            print("\tparsed score: {0}-{1} {2}-{3} {4}-{5} {6} {7}{8}:{9}{10} {11}".format(p1_set1, p2_set1, p1_set2, p2_set2, p1_set3, p2_set3, p1_serv, p1_game1, p1_game2, p2_game1, p2_game2, p2_serv))

            canvas = self.matrix.CreateFrameCanvas()
            font = graphics.Font()
            font.LoadFont("../fonts/6x10.bdf")
            
            try:
                r = int(msg[12:15])
                g = int(msg[15:18])
                b = int(msg[18:21])
                print("using {0}.{1}.{2} color".format(r, g, b))
            except:
                r = 0
                g = 255
                b = 0
                print("fallback to GREEN color")

            color_set = color_serv = color_game = graphics.Color(r, g, b)
                
            canvas.Clear()
            
            x_p1_set1 = x_p2_set1 = 0
            x_p1_set2 = x_p2_set2 = 6
            x_p1_set3 = x_p2_set3 = 12
            x_p1_game1 = x_p2_game1 = 22
            x_p1_game2 = x_p2_game2 = 27
            y_p1_set1 = y_p1_set2 = y_p1_set3 = y_p1_game1 = y_p1_game2 = 7
            y_p2_set1 = y_p2_set2 = y_p2_set3 = y_p2_game1 = y_p2_game2 = 16

            graphics.DrawText(canvas, font, x_p1_set1, y_p1_set1, color_set, p1_set1)
            graphics.DrawText(canvas, font, x_p1_set2, y_p1_set2, color_set, p1_set2)
            graphics.DrawText(canvas, font, x_p1_set3, y_p1_set3, color_set, p1_set3)
            if(p1_serv=="*"):
                graphics.DrawText(canvas, font, 17, 4, color_serv, ".")
                graphics.DrawText(canvas, font, 17, 5, color_serv, ".")
                graphics.DrawText(canvas, font, 18, 4, color_serv, ".")
                graphics.DrawText(canvas, font, 18, 5, color_serv, ".")


            graphics.DrawText(canvas, font, x_p1_game1, y_p1_game1, color_game, p1_game1)
            graphics.DrawText(canvas, font, x_p1_game2, y_p1_game2, color_game, p1_game2)
            
            graphics.DrawText(canvas, font, x_p2_set1, y_p2_set1, color_set, p2_set1)
            graphics.DrawText(canvas, font, x_p2_set2, y_p2_set2, color_set, p2_set2)
            graphics.DrawText(canvas, font, x_p2_set3, y_p2_set3, color_set, p2_set3)
            graphics.DrawText(canvas, font, x_p2_game1, y_p2_game1, color_game, p2_game1)
            if(p2_serv=="*"):
                graphics.DrawText(canvas, font, 17, 13, color_serv, ".")
                graphics.DrawText(canvas, font, 17, 14, color_serv, ".")
                graphics.DrawText(canvas, font, 18, 13, color_serv, ".")
                graphics.DrawText(canvas, font, 18, 14, color_serv, ".")
            graphics.DrawText(canvas, font, x_p2_game2, y_p2_game2, color_game, p2_game2)

            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(1)



        else:
            print("ERROR: invalid score, cannot display")


    def display(self, msg):
        print("Displaying '{0}'".format(msg))
        canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        #font.LoadFont("../fonts/6x10.bdf")
        font.LoadFont("../../fonts/9x15B.bdf")
        #font.LoadFont("../../fonts/helvR12.bdf")
        #font.LoadFont("../../fonts/tom-thumb.bdf")
        #font.LoadFont("../../fonts/texgyre-27.bdf")
        #font.LoadFont("../../fonts/10x20.bdf")

        clrWhite = graphics.Color(255, 255, 255) 
        clrRed = graphics.Color(255, 0, 0) 
        clrYellow = graphics.Color(255, 255, 0) 
        clrGreen = graphics.Color(0, 255, 0)
        clrGrey = graphics.Color(128, 128, 128)

        clrName = clrGrey
        clrScoreSet = clrName
        clrScoreGame = clrScoreSet
        
        canvas.Clear()

        """
        ## Flag 5x5 (too small)
        f1l = 10 
        f1h = 10
        f1x = 27
        f1y = 5

        fl = f1l - 1
        fh = f1h - 1
        fx = f1x
        fy = f1y
        graphics.DrawLine(canvas, fx, fy, fx + fl, fy, clrRed)
        graphics.DrawLine(canvas, fx, fy, fx, fy + fh, clrRed)
        graphics.DrawLine(canvas, fx + fl, fy, fx + fl, fy + fh, clrRed)
        graphics.DrawLine(canvas, fx, fy + fh, fx + fl, fy + fh, clrRed)
        
        graphics.DrawLine(canvas, fx + 1, fy + 1, fx + 1, fy + 1, clrRed)
        graphics.DrawLine(canvas, fx + fl - 1, fy + 1, fx + fl - 1, fy + 1, clrRed)
        graphics.DrawLine(canvas, fx + 1, fy + fh - 1, fx + 1, fy + fh - 1, clrRed)
        graphics.DrawLine(canvas, fx + fl - 1, fy + fh - 1, fx + fl - 1, fy + fh - 1, clrRed)

        graphics.DrawLine(canvas, fx + 2, fy + 1, fx + 2, fy + 1, clrWhite)
        graphics.DrawLine(canvas, fx + 2, fy + fh - 1, fx + 2, fy + fh - 1, clrWhite)
        graphics.DrawLine(canvas, fx + 1, fy + 2, fx + fl - 1, fy + 2, clrWhite)
        """
        
        ## Flag Switzerland 10x10
        f1l = 10 
        f1h = 10
        f1x = 28
        f1y = 4

        fl = f1l - 1
        fh = f1h - 1
        fx = f1x
        fy = f1y
        clrF1 = graphics.Color(218, 41, 28)
        clrF2 = clrWhite
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
        f2x = 27
        f2y = 21 

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
        xGame = 79
        xService = 73
        wSet = 12
        xSet1 = 40
        xSet2 = xSet1 + wSet
        xSet3 = xSet2 + wSet
        
        graphics.DrawText(canvas, font, 0, 14, clrName, "FED")
        graphics.DrawText(canvas, font, xSet1, 14, clrScoreSet, "7")
        graphics.DrawText(canvas, font, xSet2, 14, clrScoreSet, "3")
        graphics.DrawText(canvas, font, xSet3, 14, clrScoreSet, "5")
        graphics.DrawText(canvas, font, xService, 9, clrScoreSet, ".")
        graphics.DrawText(canvas, font, xGame, 14, clrScoreSet, "30")


        graphics.DrawText(canvas, font, 0, 31, clrName, "NAD")

        graphics.DrawText(canvas, font, xSet1, 31, clrScoreSet, "6")
        graphics.DrawText(canvas, font, xSet2, 31, clrScoreSet, "6")
        graphics.DrawText(canvas, font, xSet3, 31, clrScoreSet, "4")
        graphics.DrawText(canvas, font, xService, 31, clrScoreSet, "")
        graphics.DrawText(canvas, font, xGame, 31, clrScoreSet, "15")

        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(50)

# Main function
if __name__ == "__main__":
    simple_text = SimpleText()
    if (not simple_text.process()):
        simple_text.print_help()
    simple_text.display("Msg 2")
    simple_text.display("Msg 3")
