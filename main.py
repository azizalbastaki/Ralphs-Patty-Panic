# Written by Abdulaziz Albastaki, March 2024

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton
from direct.actor.Actor import Actor

class MyApp(ShowBase):

        def __init__(self):
            ShowBase.__init__(self)
            self.appStatus = "STARTMENU"
            self.ralphStatus = "RUN"
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

            self.keyMap = {
                "left": False,
                "right": False
            }

            self.accept("a", self.updateKey, ["left", True])
            self.accept("a-up", self.updateKey, ["left", False])

            self.accept("s", self.updateKey, ["backwards", True])
            self.accept("s-up", self.updateKey, ["backwards", False])

            self.accept("d", self.updateKey, ["right", True])
            self.accept("d-up", self.updateKey, ["right", False])

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
                # move ralph away from the camera to the left edge of the screen
                if self.ralph.getX() < -20:
                    xMovementComplete = True
                else:
                    self.ralph.setX(self.ralph, -10*dt)
                if self.ralph.getY() > 70:
                    yMovementComplete = True
                else:
                    self.ralph.setY(self.ralph, 35*dt)

                if xMovementComplete and yMovementComplete:
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

            dt = globalClock.getDt()
            currentAnim = self.ralph.getCurrentAnim()
            # make WASD controls for ralph using delta time, moves right and left only
            if self.keyMap["left"]:
                self.ralph.setY(self.ralph, -10*dt)
                if self.ralphStatus != "RUN":
                    self.ralph.loop("run")
                    self.ralphStatus = "RUN"
                self.ralph.setH(270)
            if self.keyMap["right"]:
                self.ralph.setH(90)
                self.ralph.setY(self.ralph, -10*dt)
                if self.ralphStatus != "RUN":
                    self.ralph.loop("run")
                    self.ralphStatus = "RUN"
            if not self.keyMap["left"] and not self.keyMap["right"]:
                self.ralph.stop()
                self.ralph.pose("walk", 17)
                self.ralphStatus = "IDLE"

            return task.cont

app = MyApp()
app.run()
