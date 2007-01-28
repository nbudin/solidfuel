from Text import Text
from VBox import VBox
from Box import Box
import solidfuel.constants

class TextWrapper(VBox):
    def __init__(self, text, font, color, width, padding=2.0, justify=solidfuel.constants.CENTER):
        VBox.__init__(self, padding=padding, justify=justify)
        final_lines = self._splitlines(text, font, width)
        for x in final_lines:
            if len(x):
                self.addChild(Text(font, x, color))
            else:
                s = Box()
                s.h = font.get_height()
                self.addChild(s)
        self.pack()
        
    def _splitlines(self, string, font, width):
        # Mercilessly stolen from David Clark's textrect module on PCR
        final_lines = []

        requested_lines = string.splitlines()

        for requested_line in requested_lines:
            if font.size(requested_line)[0] > width:
                words = requested_line.split(' ')
                for word in words:
                    if font.size(word)[0] >= width:
                        raise "The word " + word + " is too long to fit in the rect passed."
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    if font.size(test_line)[0] < width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)
        return final_lines