# Written by Abdulaziz Albastaki, March 2024

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton
from direct.actor.Actor import Actor
# import pointlights
from panda3d.core import PointLight
class MyApp(ShowBase):

        def __init__(self):
            ShowBase.__init__(self)
            self.appStatus = "STARTMENU"
            self.ralphStatus = "RUN"
            self.startingX = -22
            self.startingY = 70
            self.startingZ = -10

            # add an onscreen title that says "Ralph's Patty Panic" in bold
            self.title = OnscreenText(text="Ralph's Patty Panic",
                                      style=1, fg=(1, 1, 1, 1),
                                      pos=(0, 0.7), scale=0.15)

            self.setBackgroundColor(0, 0, 0, 1)
            self.button = DirectButton(text=("Start"), scale=0.1, command=self.printHello)
            self.button.setPos(0, 0, 0.3)
            self.button['text_fg'] = (0, 1, 1, 1)
            self.button['frameColor'] = (0, 0, 0, 0)

            self.name = OnscreenText(text="2024 Abdulaziz Albastaki",
                                     pos=(0, -0.95), fg=(1, 1, 1, 1),
                                     scale=0.07)

            self.ralph = Actor("assets/models/ralph",
                               {"run": "assets/models/ralph-run",
                                "walk": "assets/models/ralph-walk"})
            self.ralph.reparentTo(render)
            self.ralph.setScale(.2)
            self.ralph.setPos(0, 25, -5)
            self.ralph.setScale(1)
            self.ralph.reparentTo(render)
            self.ralph.loop("run")
            # give ralph a pointlight
            plight = PointLight('plight')
            plight.setColor((2, 2, 2, 1))
            plight.setColorTemperature(6000)
            plnp = render.attachNewNode(plight)

            plnp.setPos(0,-70,0)
            render.setLight(plnp)
            self.staircaseCoordinates = []

            self.keyMap = {
                "left": False,
                "right": False,
                "up": False,
                "down": False,
                "space": False
            }

            self.accept("a", self.updateKey, ["left", True])
            self.accept("a-up", self.updateKey, ["left", False])

            self.accept("s", self.updateKey, ["down", True])
            self.accept("s-up", self.updateKey, ["down", False])

            self.accept("d", self.updateKey, ["right", True])
            self.accept("d-up", self.updateKey, ["right", False])

            self.accept("w", self.updateKey, ["up", True])
            self.accept("w-up", self.updateKey, ["up", False])

            self.accept("space", self.updateKey, ["space", True])
            self.accept("space-up", self.updateKey, ["space", False])

            # add update to task manager update loop
            self.taskMgr.add(self.update, "update")
        # make an update loop
        def update(self, task):
            # make a delta time variable
            dt = globalClock.getDt()
            # check the status of the game
            if self.appStatus == "STARTMENU":
                self.title.show()
                self.button.show()
                self.name.show()
            elif self.appStatus == "TRANSITION_GAME":
                self.title.hide()
                self.button.hide()
                self.name.hide()
                xMovementComplete = False
                yMovementComplete = False
                zMovementComplete = False
                # move ralph away from the camera to the left edge of the screen
                if self.ralph.getX() < -20:
                    xMovementComplete = True
                else:
                    self.ralph.setX(self.ralph, -10*dt)
                if self.ralph.getY() > 70:
                    yMovementComplete = True
                else:
                    self.ralph.setY(self.ralph, 35*dt)
                if self.ralph.getZ() < -10:
                    zMovementComplete = True
                else:
                    self.ralph.setZ(self.ralph, -10*dt)

                if xMovementComplete and yMovementComplete and zMovementComplete:
                    if self.ralph.getH() < 90:
                        self.ralph.setH(self.ralph, 90*dt)
                    else:
                        self.ralph.setH(90)
                        self.appStatus = "GAME"
            elif self.appStatus == "INSTRUCTIONS":
                self.showInstructions(task)
            if self.appStatus != "GAME":
                return task.cont
            else:
                self.taskMgr.add(self.gameLoop, "update")
                self.generateMap()

                return task.done

        def updateKey(self, key, value):
            self.keyMap[key] = value
        def printHello(self):
            print('Hello World')
            self.appStatus = "TRANSITION_GAME"

        def close(self):
            print('Closing the application')
            self.destroy()

        def showInstructions(self, task):
            # create a new onscreen text object that says "Press 'SPACE' to go to the next instruction"
            self.instructions = OnscreenText(text="Press 'SPACE' to go to the next instruction",
                                             pos=(0, -0.95), fg=(1, 1, 1, 1),
                                             scale=0.07)

        def gameLoop(self, task):
            print(self.ralph.getZ())
            def makeRalphRun():
                if self.ralphStatus != "RUN":
                    self.ralph.loop("run")
                    self.ralphStatus = "RUN"

            if int(self.ralph.getX()) < -22:
                self.ralph.setX(-22)
            if self.ralph.getX() > 22:
                self.ralph.setX(22)
            if self.ralph.getZ() > 10:
                self.ralph.setZ(9.9)
            if self.ralph.getZ() < -10:
                self.ralph.setZ(-10)

            dt = globalClock.getDt()
            currentAnim = self.ralph.getCurrentAnim()
            # make WASD controls for ralph using delta time, moves right and left only
            if self.keyMap["left"]:
                self.ralph.setY(self.ralph, -10*dt)
                makeRalphRun()
                self.ralph.setH(270)

            if self.keyMap["right"]:
                self.ralph.setH(90)
                self.ralph.setY(self.ralph, -10*dt)
                makeRalphRun()

            if self.keyMap["up"]:
                ralphX = self.ralph.getX()
                for staircase in self.staircaseCoordinates:
                    if abs(ralphX-staircase) < 2:
                        self.ralph.setZ(self.ralph, 10*dt)
                        self.ralph.setH(180)
                        makeRalphRun()
                        break

            if self.keyMap["down"]:
                ralphX = self.ralph.getX()
                for staircase in self.staircaseCoordinates:
                    if abs(ralphX-staircase) < 2:
                        self.ralph.setZ(self.ralph, -10*dt)
                        self.ralph.setH(180)
                        makeRalphRun()
                        break


            if not self.keyMap["left"] and not self.keyMap["right"] and not self.keyMap["up"] and not self.keyMap["down"]:
                self.ralph.stop()
                self.ralph.pose("walk", 17)
                self.ralphStatus = "IDLE"

            return task.cont


        def generateMap(self):

            def makeBaconStairCase(xAxis):
                self.staircaseCoordinates.append(xAxis)
                for i in range(0, 10):
                    bacon = loader.loadModel("assets/models/bacon.gltf")
                    bacon.setPos(xAxis, 73, -7 + i*2)
                    bacon.setScale(3)
                    bacon.reparentTo(render)


            # make a for loop making 10 copies of the cube, next to each other
            for i in range(-1, 21):
                self.cube = loader.loadModel("models/box")
                #set the scale of the new cube to be 2
                self.cube.setScale(2)
                # set the position of the new cube to be the length of the cube away from the previous cube

                self.cube.setPos(self.ralph.getX() + i*2, self.ralph.getY(), self.ralph.getZ()-2)
                self.cube.reparentTo(render)

            self.plate = loader.loadModel("assets/models/plate.gltf")
            self.plate.setPos(9, 50, -9)
            self.plate.setScale(5)
            self.plate.reparentTo(render)

            makeBaconStairCase(-20)
            makeBaconStairCase(20)
            makeBaconStairCase(4)
            makeBaconStairCase(-8)





app = MyApp()
app.run()
