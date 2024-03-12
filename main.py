# Written by Abdulaziz Albastaki, March 2024

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode
from direct.showbase.DirectObject import DirectObject

class MyApp(ShowBase):

        def __init__(self):
            ShowBase.__init__(self)

            # add an onscreen title that says "Ralph's Patty Panic" in bold
            self.title = OnscreenText(text="Ralph's Patty Panic",
                                      style=1, fg=(1, 1, 1, 1),
                                      pos=(0, 0.5), scale=0.15)

            self.setBackgroundColor(0, 0, 0, 1)
            self.button = DirectButton(text=("Start"), scale=0.1, command=self.printHello)
            self.button.setPos(0, 0, 0)
            self.button['text_fg'] = (0, 1, 1, 1)
            self.button['frameColor'] = (0, 0, 0, 0)

            self.name = OnscreenText(text="2024 Abdulaziz Albastaki",
                                     pos=(0, -0.95), fg=(1, 1, 1, 1),
                                     scale=0.07)

        def printHello(self):
            print('Hello World')

        def close(self):
            print('Closing the application')
            self.destroy()

app = MyApp()
app.run()
