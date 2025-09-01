from PyQt6.QtCore import (Qt)

from qfluentwidgets import PushButton, setFont, ToolTipFilter


class TabCard(PushButton):

    def _postInit(self):
        super()._postInit()

        self.setEnabled(False)

        self.setStyleSheet("background-color:rgb(255,255,255);border-radius:10px")

        self.__initWidget()

    def __initWidget(self):
        setFont(self, 12)
        self.setFixedHeight(36)
        self.setMaximumWidth(240)
        self.setMinimumWidth(64)
        self.installEventFilter(ToolTipFilter(self, showDelay=1000))
        self.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
