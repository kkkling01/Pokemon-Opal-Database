from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel
from qfluentwidgets import ScrollArea


class DescriptionInterface(ScrollArea):

    def __init__(self, GameID):
        super().__init__()

        self.setFrameShape(QFrame.frameShape(self).NoFrame)

        self.setStyleSheet("background: transparent;")

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.view.setObjectName('view')

        self.vBoxLayout.addWidget(QLabel(GameID+"详情页"))
