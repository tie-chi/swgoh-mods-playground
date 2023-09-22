from dataclasses import dataclass
from enum import Enum


class StatType(Enum):
    """
    All stats types consistent with GI Optimizer's stats index
    """

    Unknown = 0
    Health = 1
    Strength = 2
    Agility = 3
    Intelligence = 4
    Speed = 5
    PhysicalDamage = 6
    SpecialDamage = 7
    UnitDefense = 8
    UnitResistance = 9
    ArmorPenetration = 10
    ResistancePenetration = 11
    DodgeRating = 12
    DeflectionRating = 13
    UnitPhysicalCriticalChance = 14
    UnitSpecialCriticalChance = 15
    CriticalDamage = 16
    Potency = 17
    Tenacity = 18
    DodgePercentAdditive = 19
    DeflectionPercentAdditive = 20
    AttackCriticalPercentAdditive = 21
    AbilityCriticalPercentAdditive = 22
    ArmorPercentAdditive = 23
    SuppressionPercentAdditive = 24
    ArmorPenetrationPercent = 25
    ResistancePenetrationPercent = 26
    HealthSteal = 27
    Protection = 28
    ShieldPenetration = 29
    HealthRegen = 30
    PhysicalDamagePercent = 31
    SpecialDamagePercent = 32
    DodgeNegatePercentAdditive = 33
    DeflectionNegatePercentAdditive = 34
    AttackCriticalNegatePercentAdditive = 35
    AbilityCriticalNegatePercentAdditive = 36
    UnitPhysicalAccuracy = 37
    UnitSpecialAccuracy = 38
    UnitPhysicalCriticalAvoidance = 39
    UnitSpecialCriticalAvoidance = 40
    Offense = 41
    Defense = 42
    DefensePenetration = 43
    EvasionRating = 44
    CriticalRating = 45
    EvasionNegateRating = 46
    CriticalNegateRating = 47
    OffensePercent = 48
    DefensePercent = 49
    DefensePenetrationPercentAdditive = 50
    EvasionPercentAdditive = 51
    Accuracy = 52
    CriticalChance = 53
    CriticalAvoidance = 54
    HealthPercent = 55
    ProtectionPercent = 56
    SpeedPercentAdditive = 57
    CounterAttackRating = 58
    Taunt = 59
    DefensePenetrationTargetPercentAdditive = 60
    Mastery = 61


class ModSet(Enum):
    Health = 1
    Offense = 2
    Defense = 3
    Speed = 4
    CriticalChance = 5
    CriticalDamage = 6
    Potency = 7
    Tenacity = 8


class ModSlot(Enum):
    Square = 1  # "Transmitter"
    Arrow = 2  # "Receiver"
    Diamond = 3  # "Processor"
    Triangle = 4  # "Holo-array"
    Circle = 5  # "Data-bus"
    Cross = 6  # "Multiplexer"


class ModState(Enum):
    Desired = "Desired"
    Incomplete = "Incomplete"
    Unmatched = "Unmatched"
    Garbage = "Garbage"


class StatBonusType(Enum):
    """
    Bonus type classification for mods' secondary stats
    """

    Speed = "Good Speed"
    Offense = "Good Offense"
    Defense = "Good Defense"
    Potency = "Good Potency"
    Tenacity = "Good Tenacity"


@dataclass
class StatBonus:
    type: StatBonusType
    badge: str
    stats: list[StatType]
    min_flat_score: int
    min_percentage: int
    min_rolls: int
    sets: list[ModSet]
    primaries: dict[ModSlot, list[StatType]]
    multiplier: float
