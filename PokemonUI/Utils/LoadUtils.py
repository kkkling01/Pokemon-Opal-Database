from PySide6.QtGui import QImage

from ..QPokeIcon.QPokeIcon import PokeIcon


ATTRIBUTE_NAMES = (
    "一般", "冰", "地面", "妖精", "岩石", "幽灵", "恶", "格斗", "毒",
    "水", "火", "电", "草", "虫", "超能", "钢", "飞行", "龙",
)
ATTRIBUTE_ICON_DIR = "./resource/pokemon/AttributeIcon"


def attribute_icon_path(attribute_name: str) -> str:
    return f"{ATTRIBUTE_ICON_DIR}/{attribute_name}.png"


def create_attribute_icon(attribute_name: str, parent=None) -> PokeIcon:
    return PokeIcon(QImage(attribute_icon_path(attribute_name)), parent)


def load_attribute_icons(parent=None) -> dict[str, PokeIcon]:
    return {
        attribute_name: create_attribute_icon(attribute_name, parent)
        for attribute_name in ATTRIBUTE_NAMES
    }
