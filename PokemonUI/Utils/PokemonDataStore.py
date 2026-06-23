import csv
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd


def _has_value(value) -> bool:
    return value is not None and not pd.isna(value) and str(value).strip() != ""


def _text(value) -> str:
    return str(value).strip() if _has_value(value) else ""


def _int(value, default: int = 0) -> int:
    if not _has_value(value):
        return default

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class PokemonRecord:
    number: str
    internal_name: str
    name: str
    attribute1: str
    attribute2: str
    hp: int
    physical_attack: int
    physical_defense: int
    speed: int
    special_attack: int
    special_defense: int
    total: int
    feature1: str
    feature2: str
    hidden_feature: str

    @classmethod
    def from_row(cls, row) -> "PokemonRecord":
        return cls(
            number=_text(row.get("序号")),
            internal_name=_text(row.get("内部名称")),
            name=_text(row.get("名称CN")),
            attribute1=_text(row.get("属性1")),
            attribute2=_text(row.get("属性2")),
            hp=_int(row.get("HP")),
            physical_attack=_int(row.get("物攻")),
            physical_defense=_int(row.get("物防")),
            speed=_int(row.get("速度")),
            special_attack=_int(row.get("特攻")),
            special_defense=_int(row.get("特防")),
            total=_int(row.get("合计")),
            feature1=_text(row.get("特性1")),
            feature2=_text(row.get("特性2")),
            hidden_feature=_text(row.get("梦特")),
        )


@dataclass(frozen=True)
class EvolutionTarget:
    from_name: str
    to_name: str
    method: str
    value: str


@dataclass(frozen=True)
class LevelUpSkill:
    level: int
    name: str


@dataclass(frozen=True)
class SkillDetail:
    name: str
    power: str
    attribute: str
    category: str
    accuracy: str
    priority: str
    description: str

    @classmethod
    def from_row(cls, row) -> "SkillDetail":
        return cls(
            name=_text(row.get("名称")),
            power=_text(row.get("威力")),
            attribute=_text(row.get("属性.1") if "属性.1" in row else row.get("属性")),
            category=_text(row.get("分类.1") if "分类.1" in row else row.get("分类")),
            accuracy=_text(row.get("命中")),
            priority=_text(row.get("先制度")),
            description=_text(row.get("描述")),
        )

    @classmethod
    def from_csv_row(cls, row: List[str]) -> "SkillDetail":
        return cls(
            name=_text(row[2] if len(row) > 2 else ""),
            power=_text(row[3] if len(row) > 3 else ""),
            attribute=_text(row[6] if len(row) > 6 else ""),
            category=_text(row[7] if len(row) > 7 else ""),
            accuracy=_text(row[8] if len(row) > 8 else ""),
            priority=_text(row[9] if len(row) > 9 else ""),
            description=_text(row[10] if len(row) > 10 else ""),
        )


class PokemonDataStore:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).resolve().parents[1] / "resource" / "pokemon" / "pokemonData"
        self._pokedex_df = None
        self._feature_desc_by_name = None
        self._evolution_df = None
        self._root_by_name = None
        self._skill_df = None
        self._skill_details = None
        self._pokemon_records = None
        self._pokemon_by_name = None
        self._skill_detail_by_name = None

    @property
    def pokedex_df(self):
        if self._pokedex_df is None:
            self._pokedex_df = pd.read_csv(
                self.data_dir / "蛋白石图鉴-图鉴.csv",
                converters={"序号": str},
            )
        return self._pokedex_df

    @property
    def evolution_df(self):
        if self._evolution_df is None:
            self._evolution_df = pd.read_csv(self.data_dir / "蛋白石图鉴-进化.csv")
        return self._evolution_df

    @property
    def skill_df(self):
        if self._skill_df is None:
            self._skill_df = pd.read_csv(self.data_dir / "蛋白石图鉴-升级招式.csv")
        return self._skill_df

    @property
    def feature_desc_by_name(self) -> Dict[str, str]:
        if self._feature_desc_by_name is None:
            data = pd.read_csv(self.data_dir / "蛋白石图鉴-特性.csv")
            self._feature_desc_by_name = {
                _text(row.get("特性cn")): _text(row.get("描述"))
                for _, row in data.iterrows()
                if _has_value(row.get("特性cn"))
            }
        return self._feature_desc_by_name

    @property
    def root_by_name(self) -> Dict[str, str]:
        if self._root_by_name is None:
            data = pd.read_csv(self.data_dir / "PokemonRoot.csv")
            self._root_by_name = {
                _text(row.get("叶精灵")): _text(row.get("根精灵"))
                for _, row in data.iterrows()
                if _has_value(row.get("叶精灵"))
            }
        return self._root_by_name

    def all_pokemon(self) -> List[PokemonRecord]:
        if self._pokemon_records is None:
            self._pokemon_records = [
                PokemonRecord.from_row(row)
                for _, row in self.pokedex_df.iterrows()
                if _has_value(row.get("名称CN"))
            ]
        return self._pokemon_records

    def pokemon_by_name(self) -> Dict[str, PokemonRecord]:
        if self._pokemon_by_name is None:
            self._pokemon_by_name = {pokemon.name: pokemon for pokemon in self.all_pokemon()}
        return self._pokemon_by_name

    def get_pokemon(self, name: str) -> Optional[PokemonRecord]:
        return self.pokemon_by_name().get(name)

    def get_pokemon_number(self, name: str) -> Optional[str]:
        pokemon = self.get_pokemon(name)
        return pokemon.number if pokemon else None

    def get_feature_desc(self, name: str) -> str:
        return self.feature_desc_by_name.get(name, "")

    def get_root_name(self, name: str) -> str:
        return self.root_by_name.get(name, name)

    def get_evolution_targets(self, from_name: str) -> List[EvolutionTarget]:
        rows = self.evolution_df[self.evolution_df["进化前"] == from_name]
        if rows.empty:
            return []

        row = rows.iloc[0]
        targets = []
        for index in range(9):
            to_name = _text(row.get(f"进化后-{index}"))
            if not to_name:
                break

            targets.append(
                EvolutionTarget(
                    from_name=from_name,
                    to_name=to_name,
                    method=_text(row.get(f"进化条件-{index}")),
                    value=_text(row.get(f"条件所需值-{index}")),
                )
            )

        return targets

    def iter_evolution_links(self, root_name: str) -> Iterable[EvolutionTarget]:
        pending = deque([root_name])
        visited = set()

        while pending:
            from_name = pending.popleft()
            if from_name in visited:
                continue

            visited.add(from_name)
            for target in self.get_evolution_targets(from_name):
                pending.append(target.to_name)
                yield target

    def get_level_up_skills(self, pokemon_name: str) -> List[LevelUpSkill]:
        rows = self.skill_df[self.skill_df["名称"] == pokemon_name]
        if rows.empty:
            return []

        row = rows.iloc[0]
        skills = []
        level_index = 2
        skill_index = 4

        while skill_index < len(row) and _has_value(row.iloc[skill_index]):
            skills.append(
                LevelUpSkill(
                    level=_int(row.iloc[level_index]),
                    name=_text(row.iloc[skill_index]),
                )
            )
            level_index += 3
            skill_index += 3

        return skills

    def all_skill_details(self) -> List[SkillDetail]:
        if self._skill_details is None:
            self._skill_details = []
            with open(self.data_dir / "蛋白石图鉴-招式.csv", encoding="utf-8-sig", newline="") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) > 11:
                        row = row[:10] + [",".join(row[10:])]

                    detail = SkillDetail.from_csv_row(row)
                    if detail.name:
                        self._skill_details.append(detail)

        return self._skill_details

    def skill_detail_by_name(self) -> Dict[str, SkillDetail]:
        if self._skill_detail_by_name is None:
            self._skill_detail_by_name = {
                detail.name: detail
                for detail in self.all_skill_details()
            }
        return self._skill_detail_by_name

    def get_skill_detail(self, skill_name: str) -> Optional[SkillDetail]:
        return self.skill_detail_by_name().get(skill_name)


_pokemon_data_store = None


def get_pokemon_data_store() -> PokemonDataStore:
    global _pokemon_data_store
    if _pokemon_data_store is None:
        _pokemon_data_store = PokemonDataStore()
    return _pokemon_data_store
