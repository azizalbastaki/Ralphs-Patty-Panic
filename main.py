# Written by Abdulaziz Albastaki, March 2024

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton
from direct.actor.Actor import Actor
# import pointlights
from panda3d.core import PointLight
from panda3d_logos.splashes import WindowSplash, RainbowSplash
from threading import Timer



class MyApp(ShowBase):

        def __init__(self):
            ShowBase.__init__(self)
            self.staircaseCoordinates = []

            self.keyMap = {
                "left": False,
                "right": False,
                "up": False,
                "down": False,
                "space": False,
                "p": False
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

            self.accept("p", self.updateKey, ["p", True])
            self.accept("p-up", self.updateKey, ["p", False])

            # add update to task manager update loop
            self.taskMgr.add(self.splashScreen, "splash")

        # make an update loop
        def setupStartingScreen(self):
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
            self.button = DirectButton(text=("Start"), scale=0.1, command=self.startgame)
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

        def splashScreen(self,task):
            splash = RainbowSplash()
            interval = splash.setup()
            interval.start()
            def tearsplashscreen():
                splash.teardown()
                self.setupStartingScreen()
                self.taskMgr.add(self.update, "update")
                return task.done
            teardownTimer = Timer(interval.get_duration()+2, tearsplashscreen)
            teardownTimer.start()

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
        def startgame(self):
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
            self.ralph.setY(70)

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
                        self.ralph.setX(staircase)
                        makeRalphRun()
                        break

            if self.keyMap["down"]:
                ralphX = self.ralph.getX()
                for staircase in self.staircaseCoordinates:
                    if abs(ralphX-staircase) < 2:
                        self.ralph.setZ(self.ralph, -10*dt)
                        self.ralph.setH(180)
                        self.ralph.setX(staircase)
                        makeRalphRun()
                        break


            if not self.keyMap["left"] and not self.keyMap["right"] and not self.keyMap["up"] and not self.keyMap["down"]:
                self.ralph.stop()
                self.ralph.pose("walk", 17)
                self.ralphStatus = "IDLE"

            # print ralph's coordinates if the 'p' key is pressed
            # make sure it only prints once.

            if self.keyMap["p"]:
                print(self.ralph.getPos())
                self.keyMap["p"] = False

            return task.cont


        def generateMap(self):

            def makeBaconStairCase(xAxis):
                self.staircaseCoordinates.append(xAxis)
                for i in range(0, 11):
                    bacon = loader.loadModel("assets/models/bacon.gltf")
                    bacon.setPos(xAxis, 70, -7 + i*2)
                    bacon.setScale(2)
                    bacon.reparentTo(render)

            def makeRowOfCubes(zaxis, xstart, xend, height=1):
                scale = 1
                for row in range(0, height):
                    for i in range(xstart, xend, scale):
                        self.cube = loader.loadModel("models/box")
                        self.cube.setScale(scale)
                        self.cube.setPos(i*scale, 80, zaxis-(scale*row))
                        self.cube.reparentTo(render)


            makeRowOfCubes(self.ralph.getZ()-2, -28, 28,2)
            makeRowOfCubes(self.ralph.getZ()+10, -8, -4)
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
