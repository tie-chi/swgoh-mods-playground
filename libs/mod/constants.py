from libs.mod.types import ModSet, ModSlot, StatBonus, StatBonusType, StatType

STAT_MIN_ROLLS = 1
STAT_MAX_ROLLS = 5

INT_VALUE_STAT_TYPES = [
    StatType.Health,
    StatType.Speed,
    StatType.Protection,
    StatType.Offense,
    StatType.Defense,
]

STAT_MIN_MAX_VALUES_DICT = {
    StatType.CriticalChance: {
        1: (0.5, 1),
        2: (0.625, 1.25),
        3: (0.75, 1.5),
        4: (1, 2),
        5: (1.125, 2.25),
        6: (1.175, 2.35),
    },
    StatType.Defense: {
        1: (2, 4),
        2: (2, 5),
        3: (3, 6),
        4: (4, 8),
        5: (4, 10),
        6: (7, 16),
    },
    StatType.DefensePercent: {
        1: (0.5, 1),
        2: (0.55, 1.1),
        3: (0.65, 1.3),
        4: (0.75, 1.5),
        5: (0.85, 1.7),
        6: (2, 4),
    },
    StatType.Health: {
        1: (99, 199),
        2: (118, 236),
        3: (150, 300),
        4: (173, 347),
        5: (214, 428),
        6: (270, 540),
    },
    StatType.HealthPercent: {
        1: (0.25, 0.5),
        2: (0.313, 0.626),
        3: (0.375, 0.75),
        4: (0.5, 1),
        5: (0.563, 1.125),
        6: (1, 2),
    },
    StatType.Offense: {
        1: (8, 16),
        2: (10, 20),
        3: (14, 28),
        4: (18, 36),
        5: (23, 46),
        6: (25, 51),
    },
    StatType.OffensePercent: {
        1: (0.125, 0.25),
        2: (0.156, 0.313),
        3: (0.188, 0.375),
        4: (0.25, 0.5),
        5: (0.281, 0.563),
        6: (0.85, 1.7),
    },
    StatType.Potency: {
        1: (0.5, 1),
        2: (0.625, 1.25),
        3: (0.75, 1.5),
        4: (1, 2),
        5: (1.125, 2.25),
        6: (1.5, 3),
    },
    StatType.Protection: {
        1: (99, 199),
        2: (154, 309),
        3: (240, 483),
        4: (319, 639),
        5: (415, 830),
        6: (460, 921),
    },
    StatType.ProtectionPercent: {
        1: (0.5, 1),
        2: (0.63, 1.25),
        3: (0.75, 1.5),
        4: (1, 2),
        5: (1.125, 2.25),
        6: (1.5, 3),
    },
    StatType.Speed: {
        1: (1, 2),
        2: (1, 3),
        3: (2, 4),
        4: (2, 5),
        5: (3, 6),
        6: (3, 6),
    },
    StatType.Tenacity: {
        1: (0.5, 1),
        2: (0.625, 1.25),
        3: (0.75, 1.5),
        4: (1, 2),
        5: (1.125, 2.25),
        6: (1.5, 3),
    },
}

STAT_BONUSES = [
    # Good Speed ⚡️
    StatBonus(
        type=StatBonusType.Speed,
        badge="⚡️",
        stats=[StatType.Speed],
        min_flat_score=53,
        min_percentage=60,
        min_rolls=3,
        sets=[ModSet.Speed],
        primaries={},
        multiplier=0.6,
    ),
    # Good Offense ⚔️
    StatBonus(
        type=StatBonusType.Offense,
        badge="⚔️",
        stats=[StatType.OffensePercent, StatType.CriticalDamage],
        min_flat_score=50,
        min_percentage=60,
        min_rolls=4,
        sets=[ModSet.CriticalChance, ModSet.CriticalDamage, ModSet.Offense],
        primaries={
            ModSlot.Triangle: [StatType.CriticalChance, StatType.CriticalDamage, StatType.OffensePercent],
            ModSlot.Cross: [StatType.OffensePercent],
        },
        multiplier=0.3,
    ),
    # Good Defense 🛡️
    StatBonus(
        type=StatBonusType.Defense,
        badge="🛡️",
        stats=[StatType.HealthPercent, StatType.ProtectionPercent, StatType.DefensePercent],
        min_flat_score=53,
        min_percentage=60,
        min_rolls=4,
        sets=[ModSet.Health, ModSet.Defense],
        primaries={
            ModSlot.Triangle: [StatType.HealthPercent, StatType.ProtectionPercent],
            ModSlot.Cross: [StatType.HealthPercent, StatType.ProtectionPercent],
        },
        multiplier=0.3,
    ),
    # Good Potency ☠️
    StatBonus(
        type=StatBonusType.Potency,
        badge="☠️",
        stats=[StatType.Potency],
        min_flat_score=52,
        min_percentage=60,
        min_rolls=3,
        sets=[ModSet.Potency],
        primaries={
            ModSlot.Cross: [StatType.Potency],
        },
        multiplier=0.2,
    ),
    # Good Tenacity ✊
    StatBonus(
        type=StatBonusType.Tenacity,
        badge="✊",
        stats=[StatType.Tenacity],
        min_flat_score=50,
        min_percentage=60,
        min_rolls=3,
        sets=[ModSet.Tenacity],
        primaries={
            ModSlot.Cross: [StatType.Tenacity],
        },
        multiplier=0.2,
    ),
]

MOD_RARITY_COLOR_DICT = {1: "Gray", 2: "Green", 3: "Blue", 4: "Purple", 5: "Golden"}
