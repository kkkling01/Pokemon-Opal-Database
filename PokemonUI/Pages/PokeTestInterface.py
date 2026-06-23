import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout
from queue import SimpleQueue
from ..QPokeIcon.QPokeIcon import PokeIcon
from PokemonUI.Utils.EvolutionUtils import format_evolution_method
from qfluentwidgets import ScrollArea, SimpleCardWidget, BodyLabel

pokeRiseQueue = SimpleQueue()


class PokeRiseCard(SimpleCardWidget):
    def __init__(self, icon, iconRise, riseDesc, parent=None):
        super().__init__(parent)

        self.setBorderRadius(20)

        self.pokeIconStart = PokeIcon(icon)
        self.pokeIconStart.setFixedSize(90, 90)
        self.pokeRiseDesc = BodyLabel(riseDesc)
        self.pokeRiseDesc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pokeIconEnd = PokeIcon(iconRise)
        self.pokeIconEnd.setFixedSize(90, 90)
        self.setBackgroundColor(QColor(255, 255, 255))
        self.setFixedHeight(130)
        self.setContentsMargins(20, 10, 20, 10)

        self.hBoxLayout = QHBoxLayout(self)
        self.initView()

    def initView(self):
        self.hBoxLayout.setContentsMargins(24, 10, 24, 10)
        self.hBoxLayout.setSpacing(18)
        self.hBoxLayout.addWidget(self.pokeIconStart, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.pokeRiseDesc, 1, Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.pokeIconEnd, 0, Qt.AlignmentFlag.AlignRight)


class PokeTestInterface(ScrollArea):

    def __init__(self):
        super().__init__()

        self.pokeRiseData = pd.read_csv(r"./resource/pokemon/pokemonData/蛋白石图鉴-进化.csv")
        self.pokeNumber = pd.read_csv(r"./resource/pokemon/pokemonData/蛋白石图鉴-图鉴.csv",
                                      converters={u'序号': str}).set_index('名称CN')['序号'].to_dict()
        self.riseDesc = ''

        self.setFrameShape(QFrame.frameShape(self).NoFrame)

        self.setStyleSheet("background: transparent;")

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.view.setObjectName('pokeView')

        self.setObjectName("PokeTest")
        self.initLayout()
        self.initView()

    def initLayout(self):
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

    def initView(self):
        pokeName = '妙蛙种子'

        pokeRiseQueue.put(pokeName)

        while True:
            if pokeRiseQueue.empty():
                break
            riseData = self.pokeRiseData[self.pokeRiseData['进化前'] == pokeRiseQueue.get()].values[0]
            if riseData[3] == '' or riseData[3] != riseData[3]:
                break
            for i in range(9):
                if riseData[(i + 1) * 3] == '' or riseData[(i + 1) * 3] != riseData[(i + 1) * 3]:
                    break
                pokeRiseQueue.put(riseData[(i + 1) * 3])

                self.riseDesc = format_evolution_method(riseData[i * 3 + 4], riseData[i * 3 + 5])

                self.vBoxLayout.addWidget(
                    PokeRiseCard(":pokemon/pokemonIcon/" + self.pokeNumber.get(riseData[2]) + ".png",
                                 ":pokemon/pokemonIcon/" + self.pokeNumber.get(riseData[(i + 1) * 3]) + ".png",
                                 self.riseDesc),
                    0,
                    Qt.AlignmentFlag.AlignTop)

    def DeleteLayout(self):
        item_list = list(range(self.vBoxLayout.count()))
        item_list.reverse()
        for i in item_list:
            item = self.vBoxLayout.itemAt(i)
            self.vBoxLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
