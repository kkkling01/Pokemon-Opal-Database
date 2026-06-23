from typing import Callable, Dict


def _value_text(value) -> str:
    return "" if value is None else str(value).strip()


EvolutionFormatter = Callable[[str], str]


EVOLUTION_METHOD_FORMATTERS: Dict[str, EvolutionFormatter] = {
    "等级": lambda value: f"等级提升至{value}级进化为",
    "物品": lambda value: f"使用{value}后进化为",
    "白天携带物品": lambda value: f"白天携带{value}升级进化为",
    "好感度": lambda value: "好感度提高后进化为",
    "招式": lambda value: f"学会{value}后升级进化为",
    "好感度白天": lambda value: "在白天，好感度提升后进化为",
    "好感度晚上": lambda value: "在晚上，好感度提升后进化为",
    "等级，攻击＞防御": lambda value: f"如果攻击＞防御，等级提升至{value}后进化为",
    "等级，攻击＜防御": lambda value: f"如果攻击＜防御，等级提升至{value}后进化为",
    "等级，攻击=防御": lambda value: f"如果攻击=防御，等级提升至{value}后进化为",
    "等级，随机": lambda value: f"等级提升至{value}后概率进化为",
    "物品雌性": lambda value: f"宝可梦为雌性时，使用{value}后进化为",
    "等级雌性": lambda value: f"宝可梦为雌性时，等级提升至{value}后进化为",
    "等级雄性": lambda value: f"宝可梦为雄性时，等级提升至{value}后进化为",
    "白天携带物": lambda value: f"白天携带{value}时，升级进化为",
}


def format_evolution_method(method: str, value) -> str:
    formatter = EVOLUTION_METHOD_FORMATTERS.get(_value_text(method))
    if formatter is None:
        return "未知进化方式"

    return formatter(_value_text(value))
