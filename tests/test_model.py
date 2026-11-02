import numpy as np
from scipy.stats import spearmanr
from src.loader import load_specs
from src.simulation import bank_efficiency, calculate_efficiency, compare, rank_agreement

def closed_form_best_k(P, C, r=0.15):
    q = 1 + r
    k_star = np.log(1 + r * C / (P * q)) / np.log(q)
    A = lambda k: min(C, P * q * (q**k - 1) / r) / k
    lo, hi = int(np.floor(k_star)), int(np.ceil(k_star))
    return lo if A(lo) >= A(hi) else hi

def test_best_bank_interval_matches_closed_form():
    for bank in (s for s in load_specs("data/farms.csv", 1) if s.is_bank):
        assert int(bank_efficiency(bank, 30).argmax()) + 1 == closed_form_best_k(bank.income, bank.bank_capacity)

def test_rank_agreement_matches_scipy():
    specs = load_specs("data/farms.csv", {"2-3-0": 11, "2-4-0": 13})
    worth = compare(specs, 60, 26_000, max_slots=20)
    eff = [calculate_efficiency(s) for s in specs]
    expected = [spearmanr(eff, worth[:, r]).statistic for r in range(60)]
    assert np.allclose(rank_agreement(specs, worth), expected)