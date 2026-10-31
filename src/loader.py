import pandas as pd
from pathlib import Path
from farm_model import FarmSpec

REQUIRED_COLUMNS = { "tier_name", "cost", "income", "is_bank", "bank_capacity" }

def load_specs(path: str | Path, collect_every: int | dict[str, int]) -> list[FarmSpec]:
    """Reads the CSV and returns one FarmSpec instance per row in the same order as the file

        collect_every - after how many rounds a bank is collected. It's either the same number for
        every bank or a dictionary of the tier name and the amount of rounds, for example: 
        {"2-3-0": 11, "2-4-0": 13}. Non-bank farms ignore it
    """

    table = pd.read_csv(path)

    # Fail early with a clear message if the file is not what we expect
    missing = REQUIRED_COLUMNS - set(table.columns)
    if missing:
        raise ValueError(f"{path} is missing the columns {sorted(missing)}")
    if table["tier_name"].duplicated().any():
        raise ValueError("Every tier_name in the CSV must be unique")

    specs = []
    for row in table.itertuples(index=False):
        is_bank = bool(row.is_bank)

        # Only banks have a capacity so we have to turn the NaN that pandas stores as None for our code
        bank_capacity = None if pd.isna(row.bank_capacity) else int(row.bank_capacity)

        # Decide the collect interval for this farm
        if not is_bank:
            interval = None

        elif isinstance(collect_every, dict):
            if row.tier_name not in collect_every:
                raise ValueError(f"No collect_every value given for the bank {row.tier_name}")

            interval = collect_every[row.tier_name]

        else:
            interval = collect_every

        specs.append(FarmSpec(
                tier_name=row.tier_name,
                cost=float(row.cost),
                income=float(row.income),
                is_bank=is_bank,
                bank_capacity=bank_capacity,
                collect_every=interval,
            ))

    return specs
