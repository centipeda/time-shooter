"""Contains mob spawners and things that create sequences of enemies."""

from tsconst import *
import tsmobs

class Spawner:
    """Spawns series of mobs, centered around a point."""
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.center = (xpos,ypos)

    def spawn(self,mobtype,color,xoffset=0,yoffset=0,xvel=0,yvel=0):
        """Spawns a single mob."""
        try: # Sanity check.
            m = getattr(tsmobs,mobtype) # Gets mob class from tsmobs
        except AttributeError:
            raise AttributeError, "Enemy type not found!"
        mob = m(self.xpos + xoffset,self.ypos + yoffset)
        mob.color = color
        mob.sketch()
        mob.update()
        return mob
    


