from dataclasses import dataclass
from libs.mod.constants import MOD_RARITY_COLOR_DICT, STAT_BONUSES, STAT_MAX_ROLLS
from libs.mod.stat import ModStat
from libs.mod.types import ModSet, ModSlot, StatType


@dataclass
class Mod:
    id: str
    set: ModSet
    slot: ModSlot
    rarity: int
    level: int
    tier: int
    primary: ModStat
    secondaries: list[ModStat]

    @property
    def scores(self) -> tuple[float, float, float]:
        """(total_score, base_score, bonus_score)"""
        return self.calculate_scores()

    @property
    def total_rolls(self) -> int:
        """(total_score, base_score, bonus_score)"""
        return sum([stat.rolls for stat in self.secondaries])

    def __str__(self) -> str:
        total_score, base_score, bonus_score = self.scores
        return " ".join(
            [
                f"Mod {self.id}",
                f"\n    ├─ {self.rarity}-dot",
                MOD_RARITY_COLOR_DICT[self.tier],
                self.set.name,
                self.slot.name,
                f"[{base_score:.0f}+{bonus_score:.0f}={total_score:.0f}]",
                "\n    ├─ Primary:",
                str(self.primary),
                "\n    └─ Secondaries:",
                *[f"{stat}[{stat.score:.0f}] " for stat in self.secondaries],
            ]
        )

    def calculate_scores(self) -> tuple[float, float, float]:
        """(total_score, mod_score, bonus_score)"""

        bonus_score: float = 0
        bonus_index: list[StatType] = []
        # bonus_record: dict[StatBonusType, int] = {}
        for bonus in STAT_BONUSES:
            bonus_stat_rolls: int = 0
            bonus_stat_score: float = 0
            sub_bonus_index: list[StatType] = []

            for stat in self.secondaries:
                if stat.type in bonus.stats:
                    bonus_stat_rolls += stat.rolls
                    bonus_stat_score += stat.score
                    sub_bonus_index.append(stat.type)

            if bonus_stat_rolls == 0:
                continue

            average_percentage = bonus_stat_score * STAT_MAX_ROLLS / bonus_stat_rolls

            if bonus_stat_rolls >= bonus.min_rolls and (
                average_percentage >= bonus.min_percentage or bonus_stat_score >= bonus.min_flat_score
            ):
                bonus_score += bonus_stat_score * bonus.multiplier
                bonus_index.extend(sub_bonus_index)

                ALIGN_BONUS = 10
                align_bonus_flag = 0
                if self.set in bonus.sets:
                    bonus_score += ALIGN_BONUS
                    align_bonus_flag += 1

                if self.slot in bonus.primaries and self.primary.type in bonus.primaries[self.slot]:
                    bonus_score += ALIGN_BONUS
                    align_bonus_flag += 1

                # bonus_record[bonus.type] = align_bonus_flag

        max_rolls = 8
        if self.rarity == 5:
            max_rolls = self.rarity + self.tier - 2

        if self.rarity == 6:
            max_rolls = self.rarity + self.tier + 1

        max_score = max_rolls * 20
        mod_score = 0
        for stat in self.secondaries:
            mod_score += stat.score
        mod_score = mod_score / max_score * 100
        total_score = mod_score + bonus_score

        return (total_score, mod_score, bonus_score)
