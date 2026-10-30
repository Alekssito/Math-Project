import numpy as np
from farm_model import FarmSpec, RunningFarm
from dataclasses import dataclass

@dataclass(frozen=True)
class SimulationResult:     # Everything a single simulation produces, one entry per round
    net_worth: np.ndarray   # Cash + sell value of all farms at the end of a round
    n_farms: np.ndarray     # Number of farms owned at the end of a round

def calculate_efficiency(spec: FarmSpec) -> float:
    """Efficiency is the income a farm made that round divided by its total cost """

    if not spec.is_bank:
        efficiency = spec.income / spec.cost
        return efficiency

    farm = RunningFarm(spec)
    collected_cash = sum(farm.cash_payout() for _ in range(spec.collect_every))
    efficiency = (collected_cash / spec.collect_every) / spec.cost 
    return efficiency

def payback_period(spec: FarmSpec) -> float:
    """Amount of rounds needed for the farms to earn back their cost"""

    return 1.0 / calculate_efficiency(spec)

