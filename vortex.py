import numpy as np
from colors import standard, alternative


class Vortex:
    def __init__(self, pos, circulation):
        self.pos = pos
        self.circulation = circulation

    @property
    def color(self):
        """Get the display colour of the vortex, indicating its circulation."""
        if self.circulation > 0:
            return standard.correct_gamma(np.abs(self.circulation))
        else:
            return alternative.correct_gamma(np.abs(self.circulation))

    def outOfBounds(self):
        """Return whether the vortex has completely left the screen."""
        self_x, self_y = self.pos
        return abs(self_x) > 10000 or abs(self_y) > 10000

    # The functions to be filled in

    def getField(self, other_pos):
        """Get the velocity induced at other_pos by the vortex, as a tuple."""
        x, y = other_pos
        self_x, self_y = self.pos
        dsquared = (x - self_x) ** 2 + (y - self_y) ** 2
        if dsquared == 0:
            return (0, 0)
        else:
            return (
                -self.circulation * (y - self_y) / dsquared,
                self.circulation * (x - self_x) / dsquared,
            )

    def moveVortex(self, vortexArray, timeStep):
        """Compute the velocity of the vortex, and move it."""
        # timeStep is how many times we move with the same velocity
        # each time the method is called.
        velocity = (0, 0)
        for otherVortex in vortexArray:
            velocity = velocity + np.array(otherVortex.getField(self.pos))
        self.pos = self.pos + timeStep * np.array(velocity)
