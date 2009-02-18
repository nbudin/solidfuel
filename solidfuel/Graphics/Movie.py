from Sprite import Sprite
import pygame.movie, pygame.surface

class Movie(Sprite):
    def __init__(self, filename):
        self._movie = pygame.movie.Movie(filename)
        surf = pygame.surface.Surface(self._movie.get_size())
        self._movie.set_display(surf)
        self._lastFrame = None
        self._movie.set_volume(0.0)
        Sprite.__init__(self, surf)

    def play(self):
        self._movie.play()

    def stop(self):
        self._movie.stop()

    def pause(self):
        self._movie.pause()

    def rewind(self):
        self._movie.rewind()

    def skip(self, seconds):
        self._movie.skip(seconds)

    def get_frame(self):
        return self._movie.get_frame()

    def get_length(self):
        return self._movie.get_length()

    def draw(self):
        if self.get_frame() != self._lastFrame:
            self.updateFromSurface()
            self._lastFrame = self.get_frame()
        Sprite.draw(self)

    def __del__(self):
        self._movie.stop()
        Sprite.__del__(self)
