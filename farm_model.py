import numpy as np
from dataclasses import dataclass
from typing import Literal

# TODO: sell rate, bank capacity

@dataclass(frozen=True)     # Freezing it to prevent errors
class FarmSpec:     # Specification for the farm
    tier_name: str      # The tier name written in a format such as "1-0-0" or "2-4-0" etc
    cost: float     # The TOTAL cost of this farm (not how much an individual upgrade costs but everything)
    income: float = 0.0      # Cash earned per round (for non-bank farms), default is 0 for bank farms
    is_bank: bool = False
    bank_deposit_cash: float = 0.0      # Deposited cash per round, works only for "X-4-X" farms and above
    bank_interest_rate: float = 0.15    # Interest per round
    bank_capacity: Literal[9500, 12500] | None = None    # The amount of cash a bank can hold (different between tier 3 and 4+)
    collect_every: int | None = None  # The rounds after which you collect the cash in the bank

    def __post_init__(self):
        if not self.is_bank:
            return
        
        middle_tier = int(self.tier_name.split("-")[1])
        expected = 9500 if middle_tier == 3 else 12500

        if self.bank_capacity != expected:
            raise ValueError(f"{self.tier_name}: capacity must be {expected}")
        if not self.collect_every or self.collect_every < 1:
            raise ValueError(f"{self.tier_name}: collect_every must be a positive integer")
        if self.bank_deposit_cash <= 0:
            raise ValueError(f"{self.tier_name}: bank_deposit_cash must be positive")
    



