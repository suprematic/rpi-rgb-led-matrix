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

        elif msg == "TEST_WHITE":
            print("\tTESTING ALL WHITE OUTPUT")
            self.display_fill(graphics.Color(239, 239, 239))
        else:
            print("ERROR: invalid score, cannot display")


    def display_fill(self, color):
        canvas = self.matrix.CreateFrameCanvas()
        canvas.Clear()
        for y in range(0,16):
            graphics.DrawLine(canvas, 0, y, 31, y, color)
        canvas = self.matrix.SwapOnVSync(canvas)

    def display(self, msg):
        print("Displaying '{0}'".format(msg))
        canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../fonts/6x10.bdf")
        textColor = graphics.Color(255, 255, 0) # yellow max
        canvas.Clear()
        graphics.DrawText(canvas, font, 0, 10, textColor, msg)
        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(1)

# Main function
if __name__ == "__main__":
    simple_text = SimpleText()

    
    if (not simple_text.process()):
        simple_text.print_help()
    # simple_text.display("Msg 2")
    # simple_text.display("Msg 3")
    for rgb in range(242,256):
        print("RGB={0}".format(rgb))
        color = graphics.Color(rgb, rgb, rgb)
        simple_text.display_fill(color)
        time.sleep(0.5)
