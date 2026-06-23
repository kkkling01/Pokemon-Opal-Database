from pathlib import Path


PACKAGE_DIR = Path(__file__).parent
RESOURCE_DIR = PACKAGE_DIR / "resource"
POKEMON_RESOURCE_DIR = RESOURCE_DIR / "pokemon"
ATTRIBUTE_ICON_DIR = POKEMON_RESOURCE_DIR / "AttributeIcon"
POKEMON_DATA_DIR = POKEMON_RESOURCE_DIR / "pokemonData"


def resource_path(*parts: str) -> Path:
    return RESOURCE_DIR.joinpath(*parts)


def pokemon_resource_path(*parts: str) -> Path:
    return POKEMON_RESOURCE_DIR.joinpath(*parts)
