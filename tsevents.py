"""Contains mob spawners and things that create sequences of enemies."""

from tsconst import *
import tsmobs

import inspect
import random

class Spawner:
    """Spawns mobs, centered around a point.
    You can decide their color, velocity, and type."""

    defcolor = random_color() # For now.
    defmob = "SquareEnemy" # Placeholder.
    
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.center = (xpos,ypos)

    def spawn(self,mobtype=defmob,behavior="stop",color=defcolor,
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

    def spawn_horiz_wall(self,xaxis,number,gap,mobtype=defmob,color=defcolor):
        """Spawns a horizontal wall of mobs, set to move forward."""
        mtype = getattr(tsmobs,mobtype)
        totalwidth = (mtype.width * number) + (gap * (number - 1))
        trumargin = float(totalwidth / number)
        start = 0
        mobs = []
        for mob in range(number):
            m = self.spawn(mobtype,color=color,behavior="straightdown",
                           xoffset=start,yoffset=xaxis)
            start += int(trumargin)
            mobs.append(m)
        return mobs
        
    def spawn_homing_squad(self,center,mobtype=defmob,color=defcolor):
        """Spawns a squad of three enemies that home in on the player's position."""
        # 30 pixels above center
        one = self.spawn(mobtype,color=color,behavior="home",
                         xoffset=center[0],yoffset=(center[1] - 30))
        # 30 pixels down, 30 pixels to the left of center
        two = self.spawn(mobtype,color=color,behavior="home",
                         xoffset=(center[0] - 30),yoffset=(center[1] + 30))
        # 30 pixels down, 30 pixels to the right of center
        three = self.spawn(mobtype,color=color,behavior="home",
                           xoffset=(center[0] + 30),yoffset=(center[1] + 30))
        return [one,two,three]

    def spawn_strafers(self,xaxis,number,gap,direction,mobtype=defmob,color=defcolor):
        """Spawns a horizontal wall of enemies, set to move left or right."""
        if "left" in direction:
            direction = "straightleft"
        elif "right" in direction:
            direction = "straightright"
        mtype = getattr(tsmobs,mobtype)
        totalwidth = (mtype.width * number) + (gap * (number - 1))
        trumargin = float(totalwidth / number)
        start = 0
        mobs = []
        for mob in range(number):
            m = self.spawn(mobtype,color=color,behavior=direction,
                           xoffset=start,yoffset=xaxis)
            start += int(trumargin)
            mobs.append(m)
        return mobs

    def spawn_seline(self,number,origin,gap,mobtype=defmob,color=defcolor):
        """Spawns a line of enemies in a diagonal line, set to move diagonally southwest."""
        curoffset = 0
        mobs = []
        for z in range(number):
            m = self.spawn(mobtype,color=color,behavior="diagsw",
                           xoffset=(origin[0] + curoffset),yoffset=(origin[1] + curoffset))
            mobs.append(m)
            curoffset += gap
        return mobs

    def spawn_swline(self,number,origin,gap,mobtype=defmob,color=defcolor):
        """Spawns a line of enemies in a diagonal line, set to move diagonally southeast."""
        curoffset = 0
        mobs = []
        for z in range(number):
            m = self.spawn(mobtype,color=color,behavior="diagse",
                           xoffset=(origin[0] - curoffset),yoffset=(origin[1] + curoffset))
            mobs.append(m)
            curoffset += gap
        return mobs

class EventGenerator:
    """Uses a Spawner to create waves of enemies."""

    def __init__(self,waveReady=False):
        self.waveReady = waveReady # Spawn enemies immediately if True.

    def choose_sequence(self):
        funcs = inspect.getmembers(Spawner)
        # This'll break if another attribute is added to Spawner.
        wavechoice = random.choice(funcs[4:])
        return wavechoice
        
    def launch_wave(self,spawner):
        wave = self.choose_sequence()
        if wave[0] == 'spawn_homing_squad':
            end = spawner.spawn_homing_squad(
                (
                    random.randint(0,WINWIDTH),random.randint(0,(WINHEIGHT / 2))
                 ))
        elif wave[0] == 'spawn_horiz_wall':
            end = spawner.spawn_horiz_wall(random.randint(0,(WINHEIGHT / 2)),
                                     random.randint(1,5),
                                           random.randint(10,100))
        elif wave[0] == 'spawn_seline':
            end = spawner.spawn_seline(random.randint(1,5),
                                       (random.randint(0,WINWIDTH),random.randint(0,(WINHEIGHT / 4))),
                                       random.randint(10,100))
        elif wave[0] == 'spawn_swline':
            end = spawner.spawn_swline(random.randint(1,5),
                                       (random.randint(0,WINWIDTH),random.randint(0,(WINHEIGHT / 4))),
                                       random.randint(10,100))
        elif wave[0] == 'spawn_strafers':
            end = spawner.spawn_strafers(random.randint(0,(WINHEIGHT / 2)),
                                         random.randint(1,5),
                                         random.randint(10,100),
                                         random.choice(["left","right"]))
        else:
            end = spawner.spawn(xoffset = random.randint(0,WINWIDTH),
                          yoffset = random.randint(0,(WINHEIGHT / 4) * 3))
        return end
