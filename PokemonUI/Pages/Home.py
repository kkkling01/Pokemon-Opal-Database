from PyQt6.QtCore import Qt, QEasingCurve, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel

from qfluentwidgets import ScrollArea, CardWidget, IconWidget, BodyLabel, CaptionLabel, PushButton, \
    TransparentToolButton, FluentIcon, PopUpAniStackedWidget


class AppCard(CardWidget):

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)

        # self.setStyleSheet("background-color:#FFFFFF")
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.openButton = PushButton('下载', self)
        self.moreButton = TransparentToolButton(FluentIcon.MORE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(100)
        self.iconWidget.setFixedSize(60, 60)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.openButton.setFixedWidth(120)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        self.moreButton.setFixedSize(32, 32)


class HomeInterface(ScrollArea):
    descriptionSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.setObjectName("home-Interface")

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.initLayout()
        self.initView()

    def initLayout(self):
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.setStyleSheet("background: transparent;")
        self.setFrameShape(QFrame.frameShape(self).NoFrame)

        self.view.setObjectName('view')

    def initView(self):
        for i in range(5):
            self.addCard(parent=self.view,
                         content="noting",
                         icon="resource/pokemon/GameIcon/PokemonZ.png",
                         title="Test"
                         )

    def addCard(self, parent, content, icon, title):
        cacheCard = AppCard(parent=parent,
                            content=content,
                            icon=icon,
                            title=title)
        self.vBoxLayout.addWidget(cacheCard)

        cacheCard.clicked.connect(lambda: self.descriptionSignal.emit(title))
