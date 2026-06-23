from PySide6.QtCore import Qt, Signal, QEasingCurve, QObject, QThread, Slot, QTimer
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLayout, QStackedLayout

from PokemonUI.QPokeIcon.QPokeIcon import PokeIcon
from PokemonUI.Utils.PokemonDataStore import get_pokemon_data_store
from PokemonUI.paths import ATTRIBUTE_ICON_DIR
from qfluentwidgets import (ImageLabel, CaptionLabel, ElevatedCardWidget, SmoothScrollArea,
                            SearchLineEdit, IndeterminateProgressRing, BodyLabel)

import PokemonUI.resource.pokeResource_rc


DEFAULT_ICON_RESOURCE_DIR = "PokeOpalIcon"


def attribute_icon_path(attribute: str) -> str:
    return str(ATTRIBUTE_ICON_DIR / f"{attribute}.png")


class PokemonCardLoadWorker(QObject):
    imagesLoaded = Signal(list)
    finished = Signal()

    def __init__(self, rows, icon_resource_dir=DEFAULT_ICON_RESOURCE_DIR):
        super().__init__()
        self.rows = rows
        self.icon_resource_dir = icon_resource_dir
        self._cancelled = False

    @Slot()
    def load(self):
        loadedCards = []
        for index, number, name, attribute1, attribute2 in self.rows:
            if self._cancelled:
                break

            image = QImage(f":pokemon/{self.icon_resource_dir}/{number}.png")
            loadedCards.append((index, name, attribute1, attribute2, image))

        if not self._cancelled:
            self.imagesLoaded.emit(loadedCards)
        self.finished.emit()

    def cancel(self):
        self._cancelled = True


class PokemonCard(ElevatedCardWidget):

    def __init__(self, Image: QImage, name: str, attribute1: str, attribute2: str = '',
                 parent: QWidget = None):
        super().__init__(parent)

        self.pokeName = name
        self.setObjectName(name)

        self.image = Image

        self.iconWidget = PokeIcon(Image, self)
        self.AttributeIcon1 = ImageLabel(attribute_icon_path(attribute1), self)
        # self.AttributeIcon1 = pokeAttDict.get(attribute1)
        self.label = CaptionLabel(name, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFixedHeight(22)
        self.iconWidget.scaledToHeight(90)
        self.AttributeIcon1.scaledToHeight(20)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(12, 12, 12, 10)
        self.vBoxLayout.setSpacing(8)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignmentFlag.AlignCenter)

        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(6)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hBoxLayout.addWidget(self.AttributeIcon1, 0, Qt.AlignmentFlag.AlignCenter)
        if attribute2 != '' and attribute2 == attribute2:
            self.AttributeIcon2 = ImageLabel(attribute_icon_path(attribute2), self)
            # self.AttributeIcon2 = pokeAttDict.get(attribute2)
            self.AttributeIcon1.scaledToHeight(15)
            self.AttributeIcon2.scaledToHeight(15)
            self.hBoxLayout.addWidget(
                self.AttributeIcon2,
                0,
                Qt.AlignmentFlag.AlignCenter)

        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)
        self.setBorderRadius(20)

        self.setFixedSize(180, 176)


class LibraryInterface(SmoothScrollArea):
    pokeDescSignal = Signal()

    def __init__(self, parent=None, icon_resource_dir=DEFAULT_ICON_RESOURCE_DIR):
        super().__init__()
        self.dataStore = get_pokemon_data_store()
        self.icon_resource_dir = icon_resource_dir

        self.parent = parent
        self.setStyleSheet("transform: translateZ(0);opacity: 0.99;")

        self.view = QWidget(self)
        self.contentView = QWidget(self.view)
        self.loadingView = QWidget(self.contentView)
        self.cardView = QWidget(self.view)

        self.FlowLayout = QGridLayout(self.cardView)
        self._cardLoadThread = None
        self._cardLoadWorker = None
        self._pokemonCards = []
        self._cardCache = {}
        self._allCardData = []
        self._filteredCardData = []
        self._renderedCardCount = 0
        self._initialPageSize = 40
        self._pageSize = 24
        self._isLoadingImages = True
        self._pendingSearchText = ""

        self.vboxLayout = QVBoxLayout(self.view)
        self.contentLayout = QStackedLayout(self.contentView)
        self.loadingLayout = QVBoxLayout(self.loadingView)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("library-Interface")

        self.searchLineEdit = SearchLineEdit(self.view)
        self.searchLineEdit.setPlaceholderText('搜索宝可梦名称')

        self.searchLineEdit.setFixedWidth(730)

        self.searchLineEdit.searchSignal.connect(lambda text: self.SearchPoke(text=text))
        self.searchLineEdit.textChanged.connect(lambda text: self.SearchPoke(text=text))
        self.searchLineEdit.clearSignal.connect(lambda: self.ClearPoke())

        self.searchLineEdit.setClearButtonEnabled(True)

        self.loadingRing = IndeterminateProgressRing(self.loadingView)
        self.loadingLabel = BodyLabel("正在加载宝可梦...", self.loadingView)
        self.loadingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._searchTimer = QTimer(self)
        self._searchTimer.setSingleShot(True)
        self._searchTimer.timeout.connect(self.applySearch)

        self.verticalScrollBar().valueChanged.connect(self.onScrollValueChanged)

        self.setScrollAnimation(Qt.Orientation.Vertical, 400, QEasingCurve())
        self.initLayout()
        self.initViewAsync()
        self.destroyed.connect(self.stopCardLoader)

    def initLayout(self):
        self.FlowLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.FlowLayout.setContentsMargins(0, 20, 0, 36)
        self.FlowLayout.setHorizontalSpacing(8)
        self.FlowLayout.setVerticalSpacing(12)
        for column in range(4):
            self.FlowLayout.setColumnMinimumWidth(column, 180)

        self.vboxLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.vboxLayout.setContentsMargins(36, 20, 36, 0)

        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.addWidget(self.loadingView)
        self.contentLayout.addWidget(self.cardView)

        self.loadingLayout.setContentsMargins(0, 140, 0, 0)
        self.loadingLayout.setSpacing(14)
        self.loadingLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.loadingLayout.addWidget(self.loadingRing, 0, Qt.AlignmentFlag.AlignHCenter)
        self.loadingLayout.addWidget(self.loadingLabel, 0, Qt.AlignmentFlag.AlignHCenter)

        self.setStyleSheet("background: transparent;")

        self.setFrameShape(QFrame.frameShape(self).NoFrame)

        self.view.setObjectName('libraryView')
        self.cardView.setObjectName('libraryCardView')

    def initViewAsync(self):
        self.vboxLayout.addWidget(self.searchLineEdit, 0, Qt.AlignmentFlag.AlignCenter)
        self.vboxLayout.addWidget(self.contentView, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.showLoading("正在加载宝可梦...")
        self.cardView.setUpdatesEnabled(False)

        rows = [
            (index, pokemon.number, pokemon.name, pokemon.attribute1, pokemon.attribute2)
            for index, pokemon in enumerate(self.dataStore.all_pokemon())
        ]

        self._cardLoadThread = QThread(self)
        self._cardLoadWorker = PokemonCardLoadWorker(rows, self.icon_resource_dir)
        self._cardLoadWorker.moveToThread(self._cardLoadThread)

        self._cardLoadThread.started.connect(self._cardLoadWorker.load)
        self._cardLoadWorker.imagesLoaded.connect(self.onImagesLoaded)
        self._cardLoadWorker.finished.connect(self._cardLoadThread.quit)
        self._cardLoadWorker.finished.connect(self._cardLoadWorker.deleteLater)
        self._cardLoadThread.finished.connect(self._cardLoadThread.deleteLater)
        self._cardLoadThread.finished.connect(self.onImageLoaderFinished)
        self._cardLoadThread.start()

    @Slot(list)
    def onImagesLoaded(self, loadedCardData):
        self._allCardData = sorted(loadedCardData, key=lambda item: item[0])
        self._isLoadingImages = False
        self.applySearch()

    def getOrCreatePokemonCard(self, cardData):
        index, name, attribute1, attribute2, image = cardData
        if index in self._cardCache:
            return self._cardCache[index]

        card = PokemonCard(
            name=name,
            attribute1=attribute1,
            attribute2=attribute2,
            Image=image,
            parent=self.cardView
        )
        card.clicked.connect(lambda card=card: self.showPokeDesc(card))
        self._cardCache[index] = card
        return card

    def addNextPage(self):
        if self._renderedCardCount >= len(self._filteredCardData):
            return

        endIndex = min(self._renderedCardCount + self._pageSize, len(self._filteredCardData))
        self.cardView.setUpdatesEnabled(False)
        for dataIndex in range(self._renderedCardCount, endIndex):
            card = self.getOrCreatePokemonCard(self._filteredCardData[dataIndex])
            visibleIndex = self.FlowLayout.count()
            self.FlowLayout.addWidget(card, visibleIndex // 4, visibleIndex % 4, Qt.AlignmentFlag.AlignCenter)
            card.show()

        self._renderedCardCount = endIndex
        self.cardView.setUpdatesEnabled(True)
        self.cardView.updateGeometry()
        self.cardView.update()

    def addInitialPage(self):
        endIndex = min(self._initialPageSize, len(self._filteredCardData))
        self.cardView.setUpdatesEnabled(False)
        for dataIndex in range(endIndex):
            card = self.getOrCreatePokemonCard(self._filteredCardData[dataIndex])
            visibleIndex = self.FlowLayout.count()
            self.FlowLayout.addWidget(card, visibleIndex // 4, visibleIndex % 4, Qt.AlignmentFlag.AlignCenter)
            card.show()

        self._renderedCardCount = endIndex
        self.cardView.setUpdatesEnabled(True)
        self.cardView.updateGeometry()
        self.cardView.update()

    @Slot()
    def onImageLoaderFinished(self):
        self._cardLoadThread = None
        self._cardLoadWorker = None

    def stopCardLoader(self, *_):
        self._isLoadingImages = False
        self.cardView.setUpdatesEnabled(True)

        if self._cardLoadWorker is not None:
            self._cardLoadWorker.cancel()

        if self._cardLoadThread is not None and self._cardLoadThread.isRunning():
            self._cardLoadThread.quit()
            self._cardLoadThread.wait(1000)

    def showPokeDesc(self, card: PokemonCard):
        pokeInformation = self.dataStore.get_pokemon(card.pokeName)
        if pokeInformation is None:
            return

        self.parent.pokeDescInterface.initView(pokeInformation, card.image)
        self.parent.stackWidget.setCurrentWidget(self.parent.pokeDescInterface)

    def ClearPoke(self):
        self.searchLineEdit.clear()
        if self._pendingSearchText:
            self.SearchPoke("")

    def SearchPoke(self, text):
        text = text.strip()
        self._pendingSearchText = text

        if self._isLoadingImages:
            return

        self.showLoading("正在搜索...")
        self._searchTimer.start(120)

    def applySearch(self):
        text = self._pendingSearchText
        self._filteredCardData = [
            cardData
            for cardData in self._allCardData
            if not text or text in cardData[1]
        ]
        self.rebuildCardGrid()
        self.hideLoading()

    def rebuildCardGrid(self):
        while self.FlowLayout.count():
            item = self.FlowLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.hide()

        self._renderedCardCount = 0
        self.addInitialPage()
        self.verticalScrollBar().setValue(0)

    def visibleCardCount(self):
        return self.FlowLayout.count()

    def onScrollValueChanged(self, value):
        scrollBar = self.verticalScrollBar()
        if self._isLoadingImages or self.contentLayout.currentWidget() is not self.cardView:
            return

        if value >= scrollBar.maximum() - 240:
            self.addNextPage()

    def showLoading(self, text):
        self.loadingLabel.setText(text)
        self.contentLayout.setCurrentWidget(self.loadingView)
        self.loadingRing.start()

    def hideLoading(self):
        self.loadingRing.stop()
        self.contentLayout.setCurrentWidget(self.cardView)
