from solidfuel.Graphics import Rectangle
from solidfuel.Controllers import Action

class ProgressBar(Rectangle):
    def __init__(self, w, h, max, start=0.0):
        Rectangle.__init__(self)
        self.w = w
        self.h = h
        
        self._progressBar = Rectangle()
        self._progressBar.borderOpacity = 0.0
        self._progressBar.fillColor = (1.0, 1.0, 1.0)
        self._progressBar.h = self.h
        self.addChild(self._progressBar)

        self._max = float(max)
        self.setProgress(start)
        
    def setProgress(self, progress):
        self._progress = progress
        self._progressBar.w = (self._progress / self._max) * self.w
        
class MakeProgress(Action):
    def __init__(self, curve, progressBar):
        Action.__init__(self, curve)
        self.progressBar = progressBar
    
    def conflictsWith(self, other):
        return (issubclass(other.__class__, MakeProgress) and self.overlaps(other) and 
                self.progressBar is other.progressBar)

    def update(self, time):
        self.progressBar.setProgress(self._curve.value(time))
        Action.update(self, time)