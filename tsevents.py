"""Contains mob spawners and things that create sequences of enemies."""

from tsconst import *
import tsmobs

class Spawner:
    """Spawns series of mobs, centered around a point."""

    defcolor = random_color()
    
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.center = (xpos,ypos)

    def spawn(self,mobtype,behavior="stop",color=defcolor,
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

    def spawn_horiz_wall(self,xaxis,number,gap,mobtype,color=defcolor):
        """Spawns a horizontal wall of mobs, set to move forward."""
        mtype = getattr(tsmobs,mobtype)
        totalwidth = (mtype.width * number) + (gap * (number - 1))
        print totalwidth
        trumargin = float(totalwidth / number)
        start = 0
        mobs = []
        for mob in range(number):
            m = self.spawn(mobtype,color=color,behavior="straightdown",
                           xoffset=start,yoffset=xaxis)
            start += int(trumargin)
            print start
            mobs.append(m)
        return mobs
        
    def spawn_homing_squad(self,center,mobtype,color=defcolor):
        """Spawns a squad of three enemies that home in on the player's position."""
        pass

    def spawn_strafers(self,xaxis,number,gap,direction,mobtype,color=defcolor):
        """Spawns a horizontal wall of enemies, set to move left or right."""
        pass

    def spawn_seline(self,center,gap,mobtype,color=defcolor):
        """Spawns a line of enemies in a diagonal line, set to move diagonally southwest."""
        pass

    def spawn_swline(self,center,gap,mobtype,color=defcolor):
        pass
