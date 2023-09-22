from libs.mod.constants import INT_VALUE_STAT_TYPES, STAT_MAX_ROLLS, STAT_MIN_MAX_VALUES_DICT
from libs.mod.types import StatType


class ModStat:
    __type: StatType
    __rolls: int
    __is_primary: bool
    __value: float
    __score: float
    # following stats are not used
    # __value_decimal: int
    # __value_decimal_unscaled: int
    # __unscaled_roll_values: list[int]
    # __stat_roller_bounds: tuple[int, int]

    @property
    def type(self) -> StatType:
        """Stat type"""
        return self.__type

    @property
    def value(self) -> float:
        """Stat value"""
        return self.__value

    @property
    def rolls(self) -> int:
        """Roll count for the stat (primary stat is always 0)"""
        return self.__rolls

    @property
    def is_primary(self) -> bool:
        return self.__is_primary

    @property
    def score(self) -> float:
        return self.__score

    def __init__(
        self,
        type: StatType,
        value_decimal: int,
        rolls: int | None = None,
        rarity: int = 0,
    ) -> None:
        self.__type = type
        self.__rolls = 0 if rolls is None else rolls
        self.__is_primary = rolls is None
        # this is just how it is calculated, taken from hotutils source code
        self.__value = int(value_decimal / 10000) if type in INT_VALUE_STAT_TYPES else value_decimal / 100
        self.__score = self.__get_score(rarity)

    def __get_score(self, mod_rarity: int) -> float:
        if self.is_primary:
            # primary stat is counted in overall mod bounus scores rather than per stat scores
            return 0

        (min_value, max_value) = STAT_MIN_MAX_VALUES_DICT[self.type][mod_rarity]
        range = max_value - min_value
        average = self.value / self.rolls

        if average < min_value:
            return 0

        # assert average >= min_value, f"{self} max={max_value}, min={min_value} average={average}, rolls={self.rolls}"

        # percentage is calculated as a normalized score within [0, 100] in average among all current rolls
        percentage = (average - min_value) / range * 100

        # score is calculated as a normalized score within [0, 100] consider the roll ratio
        score = percentage * self.rolls / STAT_MAX_ROLLS
        return score

    def __str__(self) -> str:
        roll_str = f"({self.rolls})" if self.rolls > 0 else ""
        value_str = f"{self.value:.2f}".rstrip("0").rstrip(".")
        return f"{roll_str}{self.type.name}={value_str}"
