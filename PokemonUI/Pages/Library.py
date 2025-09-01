import concurrent.futures
import threading
import time
from queue import SimpleQueue

import pandas as pd
from PyQt6.QtCore import Qt, pyqtSignal, QEasingCurve
from PyQt6.QtGui import QImage, QOpenGLContext
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout


from PokemonUI.QPokeIcon.QPokeIcon import PokeIcon
from qfluentwidgets import ImageLabel, CaptionLabel, ElevatedCardWidget, SmoothScrollArea, SearchLineEdit



import PokemonUI.resource.pokeResource_rc

pokeIconQueue = SimpleQueue()


class LoadResource:

    @staticmethod
    # @numba.jit(nopython=True)
    def readIcon(times):
        for i in range(times):
            pokeIconQueue.put(
                # QImage("./resource/pokemon/pokemonIcon/" + str(i + 1).zfill(4) + ".png")
                QImage(":pokemon/PokeOpalIcon/" + str(i + 1).zfill(4) + ".png")
            )


class PokemonCard(ElevatedCardWidget):

    def __init__(self, Image: QImage, name: str, attribute1: str, attribute2: str = '',
                 attIconPath: str = "./resource/pokemon/AttributeIcon/",
                 parent: QWidget = None):
        super().__init__(parent)

        self.pokeName = name
        self.setObjectName(name)

        self.image = Image

        self.iconWidget = PokeIcon(Image, self)
        self.AttributeIcon1 = ImageLabel(attIconPath + attribute1 + ".png", self)
        # self.AttributeIcon1 = pokeAttDict.get(attribute1)
        self.label = CaptionLabel(name, self)
        self.iconWidget.scaledToHeight(90)
        self.AttributeIcon1.scaledToHeight(20)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hBoxLayout.addWidget(self.AttributeIcon1, 0, Qt.AlignmentFlag.AlignCenter)
        if attribute2 != '' and attribute2 == attribute2:
            self.AttributeIcon2 = ImageLabel("./resource/pokemon/AttributeIcon/" + attribute2 + ".png", self)
            # self.AttributeIcon2 = pokeAttDict.get(attribute2)
            self.AttributeIcon1.scaledToHeight(15)
            self.AttributeIcon2.scaledToHeight(15)
            self.hBoxLayout.addWidget(
                self.AttributeIcon2,
                0,
                Qt.AlignmentFlag.AlignCenter)

        self.vBoxLayout.addLayout(self.hBoxLayout, 0)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.setBorderRadius(20)

        self.setFixedSize(180, 176)


class IotOpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def initializeGL(self):
        f = QOpenGLContext.currentContext().functions()
        f.glClearColor(1.0, 1.0, 1.0, 1.0)
        pass

    def resizeGL(self, w, h):
        pass

    def paintGL(self):
        pass


class LibraryInterface(SmoothScrollArea):
    pokeDescSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.PokeData = pd.read_csv(r"./resource/pokemon/pokemonData/蛋白石图鉴-图鉴.csv",
                                    converters={u'序号': str})

        self.parent = parent
        self.setStyleSheet("transform: translateZ(0);opacity: 0.99;")

        self.view = QWidget(self)

        self.FlowLayout = QGridLayout()

        self.vboxLayout = QVBoxLayout(self.view)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("library-Interface")

        self.searchLineEdit = SearchLineEdit(self.view)
        self.searchLineEdit.setPlaceholderText('搜索宝可梦名称')

        self.searchLineEdit.setFixedWidth(730)

        self.searchLineEdit.searchSignal.connect(lambda text: self.SearchPoke(text=text))
        self.searchLineEdit.clearSignal.connect(lambda: self.ClearPoke())

        self.searchLineEdit.setClearButtonEnabled(True)

        self.setScrollAnimation(Qt.Orientation.Vertical, 400, QEasingCurve())
        self.initLayout()
        # self.initView()
        self.initViewAsync()
        # self.initViewMultiCore()

    def initLayout(self):
        self.FlowLayout.setAlignment(Qt.AlignmentFlag.AlignJustify | Qt.AlignmentFlag.AlignTop)
        self.FlowLayout.setContentsMargins(0, 20, 0, 36)

        self.vboxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vboxLayout.setContentsMargins(36, 20, 36, 0)

        self.setStyleSheet("background: transparent;")

        self.setFrameShape(QFrame.frameShape(self).NoFrame)

        self.view.setObjectName('libraryView')

    def initViewAsync(self):

        rIconProcess = threading.Thread(target=LoadResource.readIcon, args=(len(self.PokeData),), name="readIcon")

        rIconProcess.start()

        for index, row in self.PokeData.iterrows():
            cacheCard = PokemonCard(
                name=row['名称CN'],
                attribute1=row['属性1'],
                attribute2=row['属性2'],
                Image=pokeIconQueue.get(),
                parent=self.view
            )

            cacheCard.clicked.connect(lambda: self.showPokeDesc())

            self.FlowLayout.addWidget(cacheCard, (index // 4), index % 4)

        self.vboxLayout.addWidget(self.searchLineEdit, Qt.AlignmentFlag.AlignCenter)
        self.vboxLayout.addLayout(self.FlowLayout)

    def showPokeDesc(self):
        pokeInformation = self.PokeData[self.PokeData['名称CN'] == self.sender().pokeName].values[0]
        self.parent.pokeDescInterface.DeleteLayout()
        self.parent.pokeDescInterface.initView(pokeInformation, self.sender().image)
        self.parent.stackWidget.setCurrentWidget(self.parent.pokeDescInterface)

    def initViewMultiCore(self):
        readDataStart = time.perf_counter()
        PokeData = pd.read_csv(r"../../resource/pokemon/pokemonData/蛋白石图鉴-图鉴.csv",
                               converters={u'序号': str})
        print("读取文件耗时{}", time.perf_counter() - readDataStart)

        def processCardMultCore(pokeCol):
            print(pokeCol)

            cacheCard = PokemonCard(
                name=pokeCol[2],
                attribute1=pokeCol[3],
                attribute2=pokeCol[4],
                Image=QImage("./resource/pokemon/pokemonIcon/" + pokeCol[0] + ".png"),
                parent=self.view
            )
            cacheCard.clicked.connect(lambda: self.pokeDescSignal.emit(pokeCol[2]))

            self.FlowLayout.addWidget(cacheCard)

        print("即将执行")

        readImageStart = time.perf_counter()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(processCardMultCore, PokeData.values)

        print("绘制卡片耗时：{}", time.perf_counter() - readImageStart)

    def initView(self):
        pass

    def ClearPoke(self):
        for i in range(self.FlowLayout.count()):
            self.FlowLayout.itemAt(i).widget().show()

    def SearchPoke(self, text):

        for i in range(self.FlowLayout.count()):

            if text in self.FlowLayout.itemAt(i).widget().pokeName:
                self.FlowLayout.itemAt(i).widget().setHidden(False)
            else:
                self.FlowLayout.itemAt(i).widget().setHidden(True)
