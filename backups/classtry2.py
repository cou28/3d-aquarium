#!/usr/bin/env python

# Author: Shao Zhang and Phil Saltzman
# Last Updated: 2015-03-13
#
# This tutorial is intended as a initial panda scripting lesson going over
# display initialization, loading models, placing objects, and the scene graph.
#
# Step 1: ShowBase contains the main Panda3D modules. Importing it
# initializes Panda and creates the window. The run() command causes the
# real-time simulation to begin

from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode, NodePath, LightAttrib
from panda3d.core import LVector3
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
import sys
from direct.interval.IntervalGlobal import *

# base = ShowBase()
from direct.gui.DirectGui import *
from panda3d.core import Point3



class fishTank(ShowBase):

    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self) # borrowed from Panda3D's showbase class

        # This code puts the standard title and instruction text on screen
        # format borrowed
        self.title = OnscreenText(text="I <3 Fish",
                                  fg=(1, 1, 1, 1), parent=base.a2dBottomRight,
                                  align=TextNode.ARight, pos=(-0.1, 0.1),
                                  shadow=(0, 0, 0, .5), scale=.08)

        # Set up key input, borrowed
        self.accept('escape', sys.exit)


        # base.disableMouse()  # Disable mouse-based camera-control
        # camera.setPos(-2, -10, 1)  # -x, -z, -y Position the camera
        # camera.setHpr(0, 0, 0)
        base.trackball.node().setPos(0, 30, -1) # starting position of the camera
        
        # images of fish rightbend, leftbend, and front
        fish1 = ["models/fish1bend-1", "models/fish1bend2-1", "models/fish1front_04", 'tex/TropicalFish01.jpg']
        pos1 = (0, -1, 0)
        mov1 = "leftCircle"
        self.newFish = self.Fish(fish1, pos1, mov1)

        fish2 = ["models/tang_right_00", "models/tang_left_01", "models/tang_02", "tex/TropicalFish02.jpg"]
        pos2 = (10, -1, -10)
        mov2 = "rightCircle"
        self.newFish2 = self.Fish(fish2, pos2, mov2)

    class Fish():

        def __init__(self, fishModel, position, move):
            # ShowBase.__init__(self)
            self.fishR = Actor(fishModel[0])  # Load our animated charachter
            
            # syntax for loading the fish from Panda3d website
            fishTex = loader.loadTexture(fishModel[3])
            self.fishR.setTexture(fishTex)
            self.fishR.reparentTo(render)

            # set a starting position for the right tail fish

            # create alternate fish the left tail position (from fish perspective)
            self.fishL = Actor(fishModel[1])  # Load our animated charachter
            self.fishL.setTexture(fishTex)
            self.fishL.reparentTo(render)
            
            self.fishFront = Actor(fishModel[2])
            self.fishFront.setTexture(fishTex) # use same previous fishTex
            self.fishFront.reparentTo(render)

            # set limits for where the fish can travel
            self.xLimits = (-20, 20)
            self.yLimits = (-20, 20)
            self.zLimits = (-10, 20)

            # start with just one model
            self.fishR.hide()
            self.fishFront.hide()

            # initialize how far the fish moves each time
            self.xPosition = position[0]
            self.yPosition = position[1]
            self.zPosition = position[2]

            self.fishL.setPos((self.xPosition, self.yPosition, self.zPosition))

            # initialize initial direction
            # change will see which direction the fish is going next time
            self.zChange = -1
            self.xChange = 0

            # initialize pitch move each time the fish turns
            self.pitchChange = 0

            # store move pattern for this instance
            self.move = move

            # moving one fish and its tial
            self.moveTail()

        def moveTailLeft(self):
            # increment the distance of the fish
            self.zPosition += self.zChange
            self.xPosition += self.xChange
            # if (self.zPosition < self.zLimits[0] or # make sure fish within bounds
            # self.zPosition > self.zLimits[1]):
            #     self.zPosition = 0
            self.fishR.hide()
            self.fishFront.hide()
            # fish is moving self.zPosition space
            self.fishL.setPos((self.xPosition, self.zPosition, 0))
            self.fishL.show()

        def moveTailRight(self):
            self.zPosition += self.zChange
            self.xPosition += self.xChange
            # if (self.zPosition < self.zLimits[0] or # make sure fish within bounds
            # self.zPosition > self.zLimits[1]):
            #     self.zPosition = 0
            self.fishL.hide()
            self.fishFront.hide()
            self.fishR.setPos((self.xPosition, self.zPosition, 0))
            self.fishR.show()

        def moveTailCenter(self):
            self.zPosition += self.zChange
            self.xPosition += self.xChange
            # if (self.zPosition < self.zLimits[0] or # make sure fish within bounds
            # self.zPosition > self.zLimits[1]):
            #     self.zPosition = 0        
            self.fishL.hide()
            self.fishR.hide()
            self.fishFront.setPos((self.xPosition, self.zPosition, 0))
            self.fishFront.show()

        # turning the fish 45 degrees each time. need to make sure to change
        # how much x and z changes according to the direction the fish is facing
        def turnFish(self):
            # want to turn right, do -45
            if self.move == "leftCircle":
                self.pitchChange = (self.pitchChange+45)%360 # turn left
            elif self.move == "rightCircle":
                self.pitchChange = (360 + self.pitchChange - 45)%360 # turn right
            
            if self.pitchChange == 0:
                self.xChange, self.zChange = 0, -1
            elif self.pitchChange == 45:
                self.xChange, self.zChange = +1, -1
            elif self.pitchChange == 90:
                self.xChange, self.zChange = +1, 0
            elif self.pitchChange == 135:
                self.xChange, self.zChange = +1, +1
            elif self.pitchChange == 180:
                self.xChange, self.zChange = 0, +1
            elif self.pitchChange == 225:
                self.xChange, self.zChange = -1, +1
            elif self.pitchChange == 270:
                self.xChange, self.zChange = -1, 0
            elif self.pitchChange == 315:
                self.xChange, self.zChange = -1, -1
            self.fishL.setHpr((self.pitchChange, 0, 0))
            self.fishR.setHpr((self.pitchChange, 0, 0))
            self.fishFront.setHpr((self.pitchChange, 0, 0))

        def moveTail(self):
            seq = Sequence() # syntax for Sequence from Panda3D library and forums
            # seq.append(Wait(.2))
            # seq.append(Func(self.moveTailRight))
            seq.append(Wait(.2))
            seq.append(Func(self.moveTailCenter))
            seq.append(Wait(.2))
            seq.append(Func(self.moveTailLeft))
            seq.append(Wait(.2))
            seq.append(Func(self.moveTailCenter))
            seq.append(Wait(.2))
            seq.append(Func(self.moveTailRight))
            seq.append(Wait(.2))
            seq.append(Func(self.turnFish))
            # seq.append(Wait(.05))
            # seq.append(Func(self.moveTailCenter))
            # seq.append(Func(self.moveTailRight))
            seq.loop()





# Now that our class is defined, we create an instance of it.
# Doing so calls the __init__ method set up above
demo = fishTank()  # Create an instance of our class
demo.run()  # Run the simulation


