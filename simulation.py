import numpy as np
from farm_model import FarmSpec, RunningFarm
from dataclasses import dataclass, replace

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


def bank_efficiency(spec: FarmSpec, max_interval: int) -> np.ndarray:
    """The efficiency for collect_every 1, 2, 3, ..., max_interval for only banks"""

    return np.array([calculate_efficiency(replace(spec, collect_every=k)) for k in range(1, max_interval + 1)]) #  Copies the farm spec with a different collect_every round


def simulate(spec: FarmSpec, n_rounds: int, starting_cash: float, max_slots: int | None = None, stop_buying_after: int | None = None, background: float = 0.0) -> SimulationResult:
    """Simulates where you reinvest all cash into copies of spec whenever affordable

        max_slots - the number of max farms that can be placed
        stop_buying_after - the last round in which a farm can be bought
        background - extra cash per round (whether cash from pops or end of round cash)
    """

    if n_rounds < 1 or starting_cash < 0:
        raise ValueError("Invalid arguments, n_rounds must be at least 1 and starting cash must not be negative")

    cash = float(starting_cash)
    farms: list[RunningFarm] = []
    net_worth = np.zeros(n_rounds)
    n_farms = np.zeros(n_rounds, dtype=int)

    for current_round in range(1, n_rounds + 1):
        may_buy = stop_buying_after is None or current_round <= stop_buying_after

        while(may_buy and cash >= spec.cost and (max_slots is None or len(farms) < max_slots)):
            cash -= spec.cost
            farms.append(RunningFarm(spec))

        cash += background + sum(farm.cash_payout() for farm in farms)

        net_worth[current_round - 1] = cash + sum(farm.sell_value() for farm in farms)
        n_farms[current_round - 1] = len(farms)

    return SimulationResult(net_worth, n_farms)


def compare(specs: list[FarmSpec], n_rounds: int, starting_cash: float, **kwargs) -> np.ndarray:
    """Runs a simulation for each farm spec and adds the the net worth into a matrix where the rows are the farms and the columns are the rounds"""

    return np.array([simulate(spec, n_rounds, starting_cash, **kwargs).net_worth for spec in specs])


def best_stop_round(spec: FarmSpec, n_rounds: int, starting_cash: float, **kwargs) -> tuple[int, np.ndarray]:
    """Calculates which last buying round maximizes the net worth
        It returns (the best round, final net worth for every stop round 0, ..., n_rounds)
    """

    final_net_worth_per_round = np.array([simulate(spec, n_rounds, starting_cash, stop_buying_after=round, **kwargs).net_worth[-1] for round in range(n_rounds + 1)])

    return int(final_net_worth_per_round.argmax()), final_net_worth_per_round 


def rank_agreement(specs: list[FarmSpec], net_worth: np.ndarray) -> np.ndarray:
    """Spearman correlation between the efficiency ranking and the net worth ranking for every round
        1 = identical order
        -1 = reversed

        Spearman = Pearson correlation of the ranks
        argsort().argsort() turns values into ranks
    """

    efficiency_ranks = np.array([calculate_efficiency(spec) for spec in specs]).argsort().argsort()
    net_worth_ranks = net_worth.argsort(axis=0).argsort(axis=0)

    return np.array([np.corrcoef(efficiency_ranks, net_worth_ranks[:, r])[0, 1] for r in range(net_worth.shape[1])])


def leader_changes(net_worth: np.ndarray) -> np.ndarray:
    """Returns the rounds in which a different farm spec takes the lead for better efficiency"""

    leaders = net_worth.argmax(axis=0)
    return np.flatnonzero(leaders[1:] != leaders[:-1]) + 2


def rank_by_round(net_worth: np.ndarray) -> np.ndarray:
    """For each round (column), farm spec indices ordered best to worst"""

    return np.argsort(-net_worth, axis=0, kind="stable")