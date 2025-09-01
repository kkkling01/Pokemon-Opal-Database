import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout
from queue import SimpleQueue
from QPokeIcon import PokeIcon
from qfluentwidgets import ScrollArea, SimpleCardWidget, BodyLabel

pokeRiseQueue = SimpleQueue()


class PokeRiseCard(SimpleCardWidget):
    def __init__(self, icon, iconRise, riseDesc, parent=None):
        super().__init__(parent)

        self.setBorderRadius(20)

        self.pokeIconStart = PokeIcon(icon)
        self.pokeIconStart.scaledToHeight(90)
        self.pokeRiseDesc = BodyLabel(riseDesc)
        self.pokeRiseDesc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pokeIconEnd = PokeIcon(iconRise)
        self.pokeIconEnd.scaledToHeight(90)
        self.setBackgroundColor(QColor(255, 255, 255))
        self.setFixedHeight(130)
        self.setContentsMargins(20, 10, 20, 10)

        self.hBoxLayout = QHBoxLayout(self)
        self.initView()

    def initView(self):
        self.hBoxLayout.addWidget(self.pokeIconStart, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.pokeRiseDesc, Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.pokeIconEnd, Qt.AlignmentFlag.AlignRight)


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

                if riseData[i * 3 + 4] == '等级':
                    self.riseDesc = "等级提升至" + riseData[i * 3 + 5] + "级进化为"
                elif riseData[i * 3 + 4] == '物品':
                    self.riseDesc = "使用" + riseData[i * 3 + 5] + "后进化为"
                elif riseData[i * 3 + 4] == '白天携带物品':
                    self.riseDesc = "白天携带" + riseData[i * 3 + 5] + "升级进化为"
                elif riseData[i * 3 + 4] == '好感度':
                    self.riseDesc = "好感度提高后进化为"
                elif riseData[i * 3 + 4] == '招式':
                    self.riseDesc = "学会" + riseData[i * 3 + 5] + "后升级进化为"
                elif riseData[i * 3 + 4] == '好感度白天':
                    self.riseDesc = "在白天，好感度提升后进化为"
                elif riseData[i * 3 + 4] == '好感度晚上':
                    self.riseDesc = "在晚上，好感度提升后进化为"
                elif riseData[i * 3 + 4] == '等级，攻击＞防御':
                    self.riseDesc = "如果攻击＞防御，等级提升至" + riseData[i * 3 + 5] + "后进化为"
                elif riseData[i * 3 + 4] == '等级，攻击＜防御':
                    self.riseDesc = "如果攻击＜防御，等级提升至" + riseData[i * 3 + 5] + "后进化为"
                elif riseData[i * 3 + 4] == '等级，攻击=防御':
                    self.riseDesc = "如果攻击=防御，等级提升至" + riseData[i * 3 + 5] + "后进化为"
                elif riseData[i * 3 + 4] == '等级，随机':
                    self.riseDesc = "等级提升至" + riseData[i * 3 + 5] + "后概率进化为"
                elif riseData[i * 3 + 4] == '物品雌性':
                    self.riseDesc = "宝可梦为雌性时，使用" + riseData[i * 3 + 5] + "后进化为"
                elif riseData[i * 3 + 4] == '等级雌性':
                    self.riseDesc = "宝可梦为雌性时，等级提升至" + riseData[i * 3 + 5] + "后进化为"
                elif riseData[i * 3 + 4] == '等级雄性':
                    self.riseDesc = "宝可梦为雄性时，等级提升至" + riseData[i * 3 + 5] + "后进化为"
                elif riseData[i * 3 + 4] == '白天携带物':
                    self.riseDesc = "白天携带" + riseData[i * 3 + 5] + "时，升级进化为"
                else:
                    self.riseDesc = "未知进化方式"

                self.vBoxLayout.addWidget(
                    PokeRiseCard(":pokemon/pokemonIcon/" + self.pokeNumber.get(riseData[2]) + ".png",
                                 ":pokemon/pokemonIcon/" + self.pokeNumber.get(riseData[(i + 1) * 3]) + ".png",
                                 self.riseDesc),
                    Qt.AlignmentFlag.AlignTop)

    def DeleteLayout(self):
        item_list = list(range(self.vBoxLayout.count()))
        item_list.reverse()
        for i in item_list:
            item = self.vBoxLayout.itemAt(i)
            self.vBoxLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
