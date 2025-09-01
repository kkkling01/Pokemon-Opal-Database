from queue import SimpleQueue

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout, QProgressBar

from PokemonUI.QPokeIcon.QPokeIcon import PokeIcon
from PokemonUI.Utils.HeaderCard import HeaderCard, HeaderCardH
from PokemonUI.Utils.TabCard import TabCard
from qfluentwidgets import ScrollArea, CaptionLabel, BodyLabel, ImageLabel, \
    CardWidget, SimpleCardWidget, Flyout, FlyoutAnimationType, FluentIcon

StyleSheet = '''
QProgressBar{
    border: 2px solid #E5E5E5;
    border-radius: 10px;

}
QProgressBar::chunk {
    border-radius: 7px;
}
#HPBar::chunk{
    background-color: #00CC00;
}
#PABar::chunk{
    background-color: #FFFF99;
}
#PBBar::chunk{
    background-color: #CC6600;
}
#SABar::chunk{
    background-color: #00CCCC;
}
#SBBar::chunk{
    background-color: #3399FF;
}
#SSBar::chunk{
    background-color: #7F00FF;
}

'''

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


class PokeDescCard(HeaderCardH):

    def __init__(self, icon, pokeName, desc, attribute1: str, attribute2: str = '',
                 attIconPath: str = "./resource/pokemon/AttributeIcon/",
                 parent=None):
        super().__init__(parent)
        self.setTitle("基本信息")
        self.iconWidget = PokeIcon(icon)
        self.setBackgroundColor(QColor(255, 255, 255))
        self.titleLabel = BodyLabel(pokeName, self)
        self.contentLabel = CaptionLabel(desc, self)

        self.AttributeIcon1 = ImageLabel(attIconPath + attribute1 + ".png", self)
        # self.AttributeIcon1 = pokeAttDict.get(attribute1)
        self.AttributeIcon1.scaledToHeight(25)

        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(170)
        self.iconWidget.setFixedSize(80, 80)
        self.setBorderRadius(20)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")

        self.viewLayout.setContentsMargins(20, 11, 11, 11)
        self.viewLayout.setSpacing(15)
        self.viewLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.viewLayout.addLayout(self.vBoxLayout)

        self.attrLayout = QVBoxLayout()
        self.attrLayout.setContentsMargins(0, 0, 0, 0)
        self.attrLayout.setSpacing(10)
        '''
        属性
        '''

        self.attrLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.attrLayout.addWidget(self.AttributeIcon1, 0, Qt.AlignmentFlag.AlignRight)
        if attribute2 != '' and attribute2 == attribute2:
            self.AttributeIcon2 = ImageLabel("./resource/pokemon/AttributeIcon/" + attribute2 + ".png", self)
            # self.AttributeIcon2 = pokeAttDict.get(attribute2)
            self.AttributeIcon2.scaledToHeight(25)
            self.attrLayout.addWidget(
                self.AttributeIcon2,
                0,
                Qt.AlignmentFlag.AlignRight)

        self.viewLayout.addLayout(self.attrLayout, 0)


class PokeFeatureCard(CardWidget):

    def __init__(self, featureName, featureDesc, parent=None):
        super().__init__(parent)

        self.setBackgroundColor(QColor(255, 255, 255))

        self.titleLabel = BodyLabel(featureName)
        self.contentLabel = CaptionLabel(featureDesc)

        self.vBoxLayout = QVBoxLayout(self)

        self.setFixedHeight(100)

        self.setBorderRadius(20)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")

        self.vBoxLayout.setContentsMargins(40, 0, 40, 0)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)


class PokeSkillCard(CardWidget):

    def __init__(self, skillLevel, skillName, parent=None):
        super().__init__(parent)

        self.setBackgroundColor(QColor(255, 255, 255))

        self.titleLabel = BodyLabel((str(int(skillLevel)) + "级" if skillLevel != 1 else "初始学会") + ":" + skillName)

        self.vBoxLayout = QVBoxLayout(self)

        self.setFixedHeight(100)

        self.setBorderRadius(20)

        self.vBoxLayout.setContentsMargins(40, 0, 40, 0)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)


class PokeBar(QWidget):
    def __init__(self, pokeBarName, pokeAName, pokeValue):
        super().__init__()
        self.setStyleSheet(StyleSheet)
        self.hBoxlayout = QHBoxLayout(self)

        self.hBoxlayout.addWidget(TabCard(pokeAName))
        self.hBoxlayout.addWidget(TabCard(str(pokeValue)))
        self.hBoxlayout.addWidget(QProgressBar(self,
                                               minimum=0,
                                               maximum=350,
                                               textVisible=False,
                                               objectName=pokeBarName, value=pokeValue), 0,
                                  Qt.AlignmentFlag.AlignVCenter)


class RaceDescCard(HeaderCard):

    def __init__(self, pokeHP, pokePAttack, pokePBlock, pokeSAttack, pokeSBlock, pokeSpeed, parent=None):
        super().__init__(parent)
        self.setTitle("宝可梦种族值")
        self.setBackgroundColor(QColor(255, 255, 255))

        self.setFixedHeight(400)

        self.setBorderRadius(20)

        self.viewLayout.setContentsMargins(65, 20, 65, 20)
        self.viewLayout.addWidget(PokeBar("HPBar", "HP", pokeHP))
        self.viewLayout.addWidget(PokeBar("PABar", "物攻", pokePAttack))
        self.viewLayout.addWidget(PokeBar("PBBar", "物防", pokePBlock))
        self.viewLayout.addWidget(PokeBar("SABar", "特攻", pokeSAttack))
        self.viewLayout.addWidget(PokeBar("SBBar", "特防", pokeSBlock))
        self.viewLayout.addWidget(PokeBar("SSBar", "速度", pokeSpeed))


class LocationCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setBorderRadius(20)
        self.localLabel = BodyLabel("查找分布位置")
        self.localLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.localLabel, Qt.AlignmentFlag.AlignCenter)


class PokeDescInterface(ScrollArea):

    def __init__(self):
        super().__init__()

        self.pokeName = ''

        self.pokeFData = pd.read_csv(r"./resource/pokemon/pokemonData/蛋白石图鉴-特性.csv").set_index('特性cn')[
            '描述'].to_dict()

        self.pokeRiseData = pd.read_csv(r"./resource/pokemon/pokemonData/蛋白石图鉴-进化.csv")
        self.pokeNumber = pd.read_csv(r"./resource/pokemon/pokemonData/蛋白石图鉴-图鉴.csv",
                                      converters={u'序号': str}).set_index('名称CN')['序号'].to_dict()
        self.pokeRoot = pd.read_csv(r"./resource/pokemon/pokemonData/PokemonRoot.csv").set_index('叶精灵')[
            '根精灵'].to_dict()
        self.riseDesc = ''

        self.pokeSkill = pd.read_csv(r"./resource/pokemon/pokemonData/蛋白石图鉴-升级招式.csv")

        self.localPoke = LocationCard()
        self.localPoke.clicked.connect(self.LocalPoke)

        self.setFrameShape(QFrame.frameShape(self).NoFrame)

        self.setStyleSheet("background: transparent;")

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.view.setObjectName('pokeView')

        self.setObjectName("PokeDesc")

        self.initLayout()

    def initLayout(self):
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

    def initView(self, pokeData, pokeImage,
                 pokeDesc='目前没有详细描述'):

        self.vBoxLayout.addWidget(PokeDescCard(pokeImage,
                                               pokeData[2],
                                               pokeDesc,
                                               pokeData[3],
                                               pokeData[4]))

        self.pokeName = pokeData[2]
        FeatureView = HeaderCard()
        FeatureView.setTitle("特性")
        FeatureView.setBorderRadius(20)

        FeatureView.viewLayout.addWidget(PokeFeatureCard(pokeData[12], self.pokeFData.get(pokeData[12])))
        if pokeData[13] != '' and pokeData[13] == pokeData[13]:
            FeatureView.viewLayout.addWidget(PokeFeatureCard(pokeData[13], self.pokeFData.get(pokeData[13])))
        if pokeData[14] != '' and pokeData[14] == pokeData[14]:
            FeatureView.viewLayout.addWidget(
                PokeFeatureCard("隐藏特性：" + pokeData[14], self.pokeFData.get(pokeData[14])))

        self.vBoxLayout.addWidget(FeatureView)

        self.vBoxLayout.addWidget(RaceDescCard(int(pokeData[5]),
                                               int(pokeData[6]),
                                               int(pokeData[7]),
                                               int(pokeData[9]),
                                               int(pokeData[10]),
                                               int(pokeData[8])))

        RiseView = HeaderCard()
        RiseView.setTitle("进化链")
        RiseView.setBorderRadius(20)
        pokeRiseQueue.put(self.pokeRoot.get(pokeData[2]))

        while not pokeRiseQueue.empty():

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

                RiseView.viewLayout.addWidget(
                    PokeRiseCard(":pokemon/pokemonIcon/" + self.pokeNumber.get(riseData[2]) + ".png",
                                 ":pokemon/pokemonIcon/" + self.pokeNumber.get(riseData[(i + 1) * 3]) + ".png",
                                 self.riseDesc),
                    Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(RiseView)

        pokeRiseSkill = self.pokeSkill[self.pokeSkill['名称'] == pokeData[2]].values[0]

        RiseSkillView = HeaderCard()
        RiseSkillView.setTitle("升级招式")
        RiseSkillView.setBorderRadius(20)
        riseFlag = 4
        while pokeRiseSkill[riseFlag] != '' and pokeRiseSkill[riseFlag] == pokeRiseSkill[riseFlag]:
            RiseSkillView.viewLayout.addWidget(PokeSkillCard(pokeRiseSkill[riseFlag - 2], pokeRiseSkill[riseFlag]))
            riseFlag += 3

        self.vBoxLayout.addWidget(RiseSkillView)

        self.vBoxLayout.addWidget(self.localPoke)

    def LocalPoke(self):
        Flyout.create(
            icon=FluentIcon.UPDATE,
            title='愚者的终点',
            content="世界",
            target=self.localPoke,
            parent=self,
            isClosable=True,
            aniType=FlyoutAnimationType.PULL_UP
        )

    def DeleteLayout(self):
        item_list = list(range(self.vBoxLayout.count()))
        item_list.reverse()
        for i in item_list:
            item = self.vBoxLayout.itemAt(i)
            self.vBoxLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
