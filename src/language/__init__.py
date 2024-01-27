from src.language import elixir, python
from enum import Enum


class LanguageType(Enum):
    ELIXIR = "elixir"
    PYTHON = "python"


SOURCE_CODE_EXTENTIONS = {
    LanguageType.ELIXIR: elixir.SOURCE_CODE_EXTENTIONS,
    LanguageType.PYTHON: python.SOURCE_CODE_EXTENTIONS,
}
