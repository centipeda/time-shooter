"""Contains mob spawners and things that create sequences of enemies."""

from tsconst import *
import tsmobs

class Spawner:
    """Spawns series of mobs, centered around a point."""
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.center = (xpos,ypos)

    def spawn(self,mobtype,color,behavior="stop",
              xoffset=0,yoffset=0):
        """Spawns a single mob."""
        try: # Sanity check.
            m = getattr(tsmobs,mobtype) # Gets mob class from tsmobs
        except AttributeError:
            raise AttributeError, "Enemy type not found!"
        mob = m(self.xpos + xoffset,self.ypos + yoffset)
        mob.color = color
        mob.behavior = behavior
        mob.sketch()
        mob.update()
        return mob

    def spawn_horiz_wall(self,xaxis,number,gap,mobtype,color):
        """Spawns a horizontal wall of mobs, set to move forward."""
        mtype = getattr(tsmobs,mobtype)
        totalwidth = (mtype.width * number) + (gap * (number - 1))
        print totalwidth
        trumargin = float(totalwidth / number)
        start = 0
        mobs = []
        for mob in range(number):
            m = self.spawn(mobtype,color,behavior="straightdown",
                           xoffset=start,yoffset=xaxis)
            start += int(trumargin)
            print start
            mobs.append(m)
        return mobs
        
