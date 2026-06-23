# coding:utf-8
import sys
import time

from PySide6.QtCore import Qt, Signal, QEasingCurve, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication, QFrame, QWidget
from qframelesswindow import FramelessWindow, TitleBar

from PokemonUI.Pages.GameDescription import DescriptionInterface
from PokemonUI.Pages.Home import HomeInterface
from PokemonUI.Pages.Library import LibraryInterface
from PokemonUI.Pages.PokeDescInterface import PokeDescInterface
from PokemonUI.Pages.PokeTestInterface import PokeTestInterface
from PokemonUI.paths import RESOURCE_DIR
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationBar, NavigationItemPosition, MessageBox,
                            isDarkTheme, SearchLineEdit,
                            PopUpAniStackedWidget)


#
# AttrArray = ["一般", "冰", "地面", "妖精", "岩石", "幽灵", "恶", "格斗", "毒", "水", "火", "电", "草", "虫", "超能",
#              "钢", "飞行", "龙"]
# PokeAttIcArray = [PokeIcon(QImage(str(RESOURCE_DIR / "pokemon" / "AttributeIcon" / f"{AName}.png"))) for AName in AttrArray]

# pokeAttDict = dict(zip(
#     ["一般", "冰", "地面", "妖精", "岩石", "幽灵", "恶", "格斗", "毒", "水", "火", "电", "草", "虫", "超能",
#      "钢", "飞行", "龙"],
#     [PokeIcon(QImage(str(RESOURCE_DIR / "pokemon" / "AttributeIcon" / f"{AName}.png"))) for AName in
#      ["一般", "冰", "地面", "妖精", "岩石", "幽灵", "恶", "格斗", "毒", "水", "火", "电", "草", "虫", "超能",
#       "钢", "飞行", "龙"]]
# ))


class Widget(QWidget):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class StackedWidget(QFrame):
    """ Stacked widget """

    currentChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=False):
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.Type.InQuad)
            # widget, True, False, 200, QEasingCurve.Type.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class CustomTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 20)
        self.hBoxLayout.insertWidget(
            1, self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(
            2, self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        # add search line edit
        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setPlaceholderText('搜索应用、游戏、电影、设备等')
        self.searchLineEdit.setFixedWidth(400)
        self.searchLineEdit.setClearButtonEnabled(True)


        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))

    def resizeEvent(self, e):
        self.searchLineEdit.move((self.width() - self.searchLineEdit.width()) // 2, 8)


class IodOpenGLFrame(QOpenGLWidget):
    def initializeGL(self):
        pass

    def paintGL(self):
        pass

    def paintEvent(self, e):
        pass


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # use dark theme mode
        # setTheme(Theme.DARK)

        # change the theme color
        # setThemeColor('#0078d4')

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self.stackWidget = StackedWidget(self)

        # create sub interface

        self.homeInterface = HomeInterface()

        self.DescriptionInterface = DescriptionInterface("Nothing")

        self.appInterface = Widget('Application Interface', self)
        self.videoInterface = Widget('Video Interface', self)
        self.pokeInterface = IodOpenGLFrame(self.videoInterface)

        self.libraryInterface = LibraryInterface(parent=self)
        self.pokeDescInterface = PokeDescInterface()

        self.pokeTestInterface = PokeTestInterface()

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        navstart = time.perf_counter()
        self.initNavigation()

        print("追加导航栏时间：", time.perf_counter() - navstart)

        self.initWindow()
        ###########################

        self.updateFrameless()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', selectedIcon=FIF.HOME_FILL)
        self.addSubInterface(self.appInterface, FIF.APPLICATION, '应用')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, '视频')

        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '库', NavigationItemPosition.BOTTOM,
                             FIF.LIBRARY_FILL)
        self.navigationBar.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        # 详情页

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.navigationBar.setCurrentItem(self.homeInterface.objectName())

        self.stackWidget.addWidget(self.DescriptionInterface)
        self.homeInterface.descriptionSignal.connect(self.ToDescription)

        self.stackWidget.addWidget(self.pokeDescInterface)


        self.addSubInterface(self.pokeTestInterface, FIF.TAG, '测试')

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(str(RESOURCE_DIR / "logo.png")))
        self.setWindowTitle('宝可梦助手')
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, selectedIcon=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
            position=position,
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(RESOURCE_DIR / color / "demo.qss", encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def ToDescription(self, GameID):
        # self.stackWidget.setCurrentWidget(widget=widget)

        self.stackWidget.setCurrentWidget(self.DescriptionInterface)
        print(GameID)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))


if __name__ == '__main__':
    appstart = time.perf_counter()
    app = QApplication(sys.argv)

    w = Window()
    # w.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    # w.setWindowIcon(QIcon(str(RESOURCE_DIR / "logo.png")))
    w.show()
    print("开启时间：", time.perf_counter() - appstart)
    sys.exit(app.exec())
