from dataclasses import dataclass
from typing import Literal

SELL_RATE = 0.75
SALVAGE_BONUS = 0.10


@dataclass(frozen=True)     # Freezing it to prevent errors
class FarmSpec:     # Specification for the farm
    tier_name: str      # The tier name written in a format such as "1-0-0" or "2-4-0" etc
    cost: float     # The TOTAL cost of this farm (not how much an individual upgrade costs but everything)
    income: float = 0.0      # Cash earned per round (for non-bank farms), default is 0 for bank farms
    is_bank: bool = False
    bank_interest_rate: float = 0.15    # Interest per round
    bank_capacity: Literal[9500, 12500] | None = None    # The amount of cash a bank can hold (different between tier 3 and 4+)
    collect_every: int | None = None    # The rounds after which you collect the cash in the bank

    def __post_init__(self):
        if not self.is_bank:
            return
        
        middle_tier = int(self.tier_name.split("-")[1])     # Middle path validation
        expected = 9500 if middle_tier == 3 else 12500

        if self.bank_capacity != expected:
            raise ValueError(f"{self.tier_name}: capacity must be {expected}")
        if not self.collect_every or self.collect_every < 1:
            raise ValueError(f"{self.tier_name}: collect_every must be a positive integer")

    @property
    def sell_rate(self) -> float:
        bottom_tier = int(self.tier_name.split("-")[2])   # Checks if it's the bottom path, since it has an increased sellback
        return SELL_RATE + (SALVAGE_BONUS if bottom_tier >= 2 else 0.0)   # Later this gets returned in the RunningFarm class


class RunningFarm: # A usable running instance of a farm using the specification from the class FarmSpec

    def __init__(self, spec: FarmSpec):
        self.spec = spec
        self.balance = 0.0
        self.age = 0

    def cash_payout(self) -> float:
        s = self.spec
        if not s.is_bank:
            return s.income

        # Adds up the bank balance with its one in the previous round along with deposited cash (if any) and the interest
        self.balance = min(s.bank_capacity, (self.balance + s.income) * (1 + s.bank_interest_rate))  

        self.age += 1   # Increases the amount of passed rounds
        if self.age % s.collect_every == 0:     
            payout, self.balance = self.balance, 0.0    # Cash collected per s.collect_every round -> balance goes to 0 and we collect the payout
            return payout

        return 0.0

    def sell_value(self) -> float:
        return self.spec.sell_rate * self.spec.cost + self.balance