#!/usr/bin/env python
# Display a simple text
from samplebase import SampleBase
from rgbmatrix import graphics
import time


class SimpleText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to display on the RGB LED panel", default="Hello!")
        
    def run(self):
        msg = self.args.text
        print("Displaying '{0}'".format(msg))
        canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../fonts/6x10.bdf")
        textColor = graphics.Color(255, 255, 0)
        canvas.Clear()
        graphics.DrawText(canvas, font, 0, 10, textColor, msg)
        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(1)

# Main function
if __name__ == "__main__":
    simple_text = SimpleText()
    if (not simple_text.process()):
        simple_text.print_help()
