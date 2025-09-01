from PyQt6.QtGui import QImage

from QPokeIcon import PokeIcon

pokeAttDict = dict(zip(
        ["一般", "冰", "地面", "妖精", "岩石", "幽灵", "恶", "格斗", "毒", "水", "火", "电", "草", "虫", "超能",
         "钢", "飞行", "龙"],
        [PokeIcon(QImage("./resource/pokemon/AttributeIcon/" + AName + ".png")) for AName in
         ["一般", "冰", "地面", "妖精", "岩石", "幽灵", "恶", "格斗", "毒", "水", "火", "电", "草", "虫", "超能",
          "钢", "飞行", "龙"]]
    ))

# class pokeAtt(Enum):
#     pokeAttDict = dict(zip(
#         ["一般", "冰", "地面", "妖精", "岩石", "幽灵", "恶", "格斗", "毒", "水", "火", "电", "草", "虫", "超能",
#          "钢", "飞行", "龙"],
#         [PokeIcon(QImage("./resource/pokemon/AttributeIcon/" + AName + ".png")) for AName in
#          ["一般", "冰", "地面", "妖精", "岩石", "幽灵", "恶", "格斗", "毒", "水", "火", "电", "草", "虫", "超能",
#           "钢", "飞行", "龙"]]
#     ))