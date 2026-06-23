from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QImage
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout, QProgressBar

from PokemonUI.QPokeIcon.QPokeIcon import PokeIcon
from PokemonUI.Utils.EvolutionUtils import format_evolution_method
from PokemonUI.Utils.HeaderCard import HeaderCard, HeaderCardH
from PokemonUI.Utils.PokemonDataStore import get_pokemon_data_store
from PokemonUI.Utils.TabCard import TabCard
from PokemonUI.paths import ATTRIBUTE_ICON_DIR
from qfluentwidgets import ScrollArea, CaptionLabel, BodyLabel, ImageLabel, \
    CardWidget, SimpleCardWidget, Flyout, FlyoutAnimationType, FluentIcon, TransparentToolButton

import PokemonUI.resource.pokeResource_rc

DEFAULT_ICON_RESOURCE_DIR = "PokeOpalIcon"


def attribute_icon_path(attribute: str) -> str:
    return str(ATTRIBUTE_ICON_DIR / f"{attribute}.png")


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


class PokeRiseCard(SimpleCardWidget):
    def __init__(self, icon, iconRise, riseDesc, fromName='', toName='', onPokemonClicked=None, parent=None):
        super().__init__(parent)
        self.fromName = fromName
        self.toName = toName
        self.onPokemonClicked = onPokemonClicked

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
        self.pokeIconStart.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pokeIconEnd.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pokeIconStart.clicked.connect(lambda: self._emitPokemonClicked(self.fromName))
        self.pokeIconEnd.clicked.connect(lambda: self._emitPokemonClicked(self.toName))
        self.initView()

    def initView(self):
        self.hBoxLayout.setContentsMargins(24, 10, 24, 10)
        self.hBoxLayout.setSpacing(18)
        self.hBoxLayout.addWidget(self.pokeIconStart, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.pokeRiseDesc, 1, Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.pokeIconEnd, 0, Qt.AlignmentFlag.AlignRight)

    def _emitPokemonClicked(self, pokemonName):
        if self.onPokemonClicked is not None and pokemonName:
            self.onPokemonClicked(pokemonName)


class PokeDescCard(HeaderCardH):

    def __init__(self, icon, pokeName, desc, attribute1: str, attribute2: str = '',
                 parent=None):
        super().__init__(parent)
        self.setTitle("基本信息")
        self.iconWidget = PokeIcon(icon)
        self.setBackgroundColor(QColor(255, 255, 255))
        self.titleLabel = BodyLabel(pokeName, self)
        self.contentLabel = CaptionLabel(desc, self)

        self.AttributeIcon1 = ImageLabel(attribute_icon_path(attribute1), self)
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
            self.AttributeIcon2 = ImageLabel(attribute_icon_path(attribute2), self)
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
        self.skillName = skillName

        self.setBackgroundColor(QColor(255, 255, 255))
        self.setClickEnabled(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

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
        self.vBoxLayout.addWidget(self.localLabel, 0, Qt.AlignmentFlag.AlignCenter)


class PokeDescInterface(ScrollArea):
    backRequested = Signal()

    def __init__(self, icon_resource_dir=DEFAULT_ICON_RESOURCE_DIR):
        super().__init__()

        self.pokeName = ''
        self.dataStore = get_pokemon_data_store()
        self.icon_resource_dir = icon_resource_dir
        self.riseDesc = ''

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
        self.DeleteLayout()
        self.pokeName = pokeData.name

        self.vBoxLayout.addWidget(self.build_header())
        self.vBoxLayout.addWidget(self.build_basic_info(pokeData, pokeImage, pokeDesc))
        self.vBoxLayout.addWidget(self.build_features(pokeData))
        self.vBoxLayout.addWidget(self.build_stats(pokeData))
        self.vBoxLayout.addWidget(self.build_evolution(pokeData))
        self.vBoxLayout.addWidget(self.build_skills(pokeData))
        self.vBoxLayout.addWidget(self.build_location())

    def build_header(self):
        header = QWidget(self.view)
        header.setFixedHeight(38)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        backButton = TransparentToolButton(FluentIcon.LEFT_ARROW, header)
        backButton.setFixedSize(38, 38)
        backButton.setToolTip("返回")
        backButton.clicked.connect(self.backRequested)

        layout.addWidget(backButton, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch(1)
        return header

    def build_basic_info(self, pokeData, pokeImage, pokeDesc):
        return PokeDescCard(pokeImage,
                            pokeData.name,
                            pokeDesc,
                            pokeData.attribute1,
                            pokeData.attribute2)

    def build_features(self, pokeData):
        FeatureView = HeaderCard()
        FeatureView.setTitle("特性")
        FeatureView.setBorderRadius(20)

        FeatureView.viewLayout.addWidget(PokeFeatureCard(pokeData.feature1,
                                                         self.dataStore.get_feature_desc(pokeData.feature1)))
        if pokeData.feature2:
            FeatureView.viewLayout.addWidget(PokeFeatureCard(pokeData.feature2,
                                                             self.dataStore.get_feature_desc(pokeData.feature2)))
        if pokeData.hidden_feature:
            FeatureView.viewLayout.addWidget(
                PokeFeatureCard("隐藏特性：" + pokeData.hidden_feature,
                                self.dataStore.get_feature_desc(pokeData.hidden_feature)))

        return FeatureView

    def build_stats(self, pokeData):
        return RaceDescCard(pokeData.hp,
                            pokeData.physical_attack,
                            pokeData.physical_defense,
                            pokeData.special_attack,
                            pokeData.special_defense,
                            pokeData.speed)

    def build_evolution(self, pokeData):
        RiseView = HeaderCard()
        RiseView.setTitle("进化链")
        RiseView.setBorderRadius(20)
        rootName = self.dataStore.get_root_name(pokeData.name)

        for evolution in self.dataStore.iter_evolution_links(rootName):
            self.riseDesc = format_evolution_method(evolution.method, evolution.value)
            fromNumber = self.dataStore.get_pokemon_number(evolution.from_name)
            toNumber = self.dataStore.get_pokemon_number(evolution.to_name)
            if not fromNumber or not toNumber:
                continue

            RiseView.viewLayout.addWidget(
                PokeRiseCard(self.pokemon_icon_path(fromNumber),
                             self.pokemon_icon_path(toNumber),
                             self.riseDesc,
                             evolution.from_name,
                             evolution.to_name,
                             self.show_pokemon_detail),
                0,
                Qt.AlignmentFlag.AlignTop)

        return RiseView

    def pokemon_icon_path(self, number: str) -> str:
        return f":pokemon/{self.icon_resource_dir}/{number}.png"

    def build_skills(self, pokeData):
        RiseSkillView = HeaderCard()
        RiseSkillView.setTitle("升级招式")
        RiseSkillView.setBorderRadius(20)
        for skill in self.dataStore.get_level_up_skills(pokeData.name):
            skillCard = PokeSkillCard(skill.level, skill.name)
            skillCard.clicked.connect(lambda name=skill.name, card=skillCard: self.show_skill_detail(name, card))
            RiseSkillView.viewLayout.addWidget(skillCard)

        return RiseSkillView

    def show_pokemon_detail(self, pokemonName):
        pokemon = self.dataStore.get_pokemon(pokemonName)
        if pokemon is None:
            return

        self.initView(pokemon, QImage(self.pokemon_icon_path(pokemon.number)))
        self.verticalScrollBar().setValue(0)

    def show_skill_detail(self, skillName, target):
        detail = self.dataStore.get_skill_detail(skillName)
        if detail is None:
            content = "暂无该招式的详细效果。"
        else:
            content = (
                f"属性：{detail.attribute or '未知'}\n"
                f"分类：{detail.category or '未知'}\n"
                f"威力：{detail.power or '-'}\n"
                f"命中：{detail.accuracy or '-'}\n"
                f"先制度：{detail.priority or '0'}\n\n"
                f"{detail.description or '暂无描述。'}"
            )

        Flyout.create(
            title=skillName,
            content=content,
            target=target,
            parent=self,
            isClosable=True,
            aniType=FlyoutAnimationType.PULL_UP,
        )

    def build_location(self):
        self.localPoke = LocationCard()
        self.localPoke.clicked.connect(self.LocalPoke)
        return self.localPoke

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
        while self.vBoxLayout.count():
            item = self.vBoxLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.hide()
                widget.setParent(None)
                widget.deleteLater()
