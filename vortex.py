import numpy as np
from colors import standard, alternative


class Vortex:
    def __init__(self, pos, circulation, velocity=(0, 0)):
        self.pos = pos
        self.circulation = circulation
        self.velocity = velocity

    @property
    def color(self):
        """Get the display colour of the vortex, indicating its circulation."""
        if self.circulation > 0:
            return standard.correct_gamma(np.abs(self.circulation))
        else:
            return alternative.correct_gamma(np.abs(self.circulation))

    def outOfBounds(self):
        """Return whether the vortex has completely left the screen."""
        selfX, selfY = self.pos
        return abs(selfX) > 10000 or abs(selfY) > 10000

    # The functions to be filled in

    def getInducedVelocity(self, otherPos):
        """
        Get the velocity contribution that this vortex
        induces at otherPos, as a tuple.
        """
        otherX, otherY = otherPos
        selfX, selfY = self.pos
        distSquared = (otherX - selfX) ** 2 + (otherY - selfY) ** 2
        if distSquared == 0:
            return (0, 0)
        else:
            return (
                -self.circulation * (otherY - selfY) / distSquared,
                self.circulation * (otherX - selfX) / distSquared,
            )

    def computeVelocity(self, vortexArray):
        """
        Compute and set the velocity of this vortex by combining
        the contributions from all surrounding vortices.
        """
        self.velocity = (0, 0)
        for otherVortex in vortexArray:
            self.velocity = self.velocity + np.array(
                otherVortex.getInducedVelocity(self.pos)
            )

    def move(self, timePeriod):
        """
        Move this vortex over the specified time
        period, updating its position.
        """
        self.pos = self.pos + timePeriod * np.array(self.velocity)
