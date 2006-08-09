class Transition:
    def __init__(self, curve):
        self.curve = curve

    def update(self, time):
        raise "This is an abstract method."

class Fade(Transition):
    def __init__(self, curve, sprite):
        Transition.__init__(self, curve)
        self.sprite = sprite

    def update(self, time):
        self.sprite.opacity = self.curve.value(time)
