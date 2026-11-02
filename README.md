# BTD6 Banana Farms: does efficiency predict net worth?

A math and Python project about the Banana Farm tower in [Bloons TD 6](https://www.bloonswiki.com/Bloons_TD_6).

## Research question

> How well does a farm's efficiency predict its net worth after N rounds when its income is reinvested, and under which conditions does the prediction fail?

**Efficiency** is ε = (average cash per round) / (total cost of the farm). Its inverse, 1/ε, is the payback period in rounds. **Net worth** is cash on hand plus the sell value of every farm. All builds start with the same budget and reinvest their income into more copies of the same farm.

## Key results

*(Numbers from the current notebook run. Update them if you change the data.)*

- **Bank collection interval.** Waiting longer helps while the balance is below its capacity (the average payout rises) and hurts after that (it falls like C/k). The best interval is 11 rounds for the 2-3-0 bank and 13 for the 2-4-0. This is derived analytically in the notebook and matches the simulation.
- **Efficiency ranking.** The 2-3-0 bank is the most efficient build by a wide margin (ε ≈ 0.12), followed by 4-2-0, 0-2-3 and 2-0-3. 2-0-2 ranks last because the extra sellback does not produce cash.
- **Does ε predict the ranking?** With unlimited slots, the Spearman correlation between the ε ranking and the net-worth ranking is about 0.82 to 0.84 from round 29 on. With limited slots it drops to 0.64 (20 slots), 0.53 (10 slots) and 0.42 (5 slots) at round 60.
- **Where it fails.** Limited space, very expensive builds that cannot be reinvested in small steps, the lumpy payout of banks, and the sell loss near the end of the horizon.
- **When to stop buying.** A farm bought in round r only pays off if `(N - r + 1) * income > (1 - sell_rate) * cost`. The simulation agrees with this formula.

## How to run

1. Install Python 3.10 or newer.
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Open `project.ipynb` in Jupyter and choose *Restart & Run All*.
4. Run the tests from the repository root:
   ```bash
   python -m pytest
   ```


## Data and assumptions

- **Game version:** *57.4*
- **Difficulty and Monkey Knowledge:** Medium prices with full Monkey Knowledge. Costs in `farms.csv` use the Flat Pack Buildings discount (the base farm costs 1225). Income uses More Valuable Bananas, and bank capacities use Bigger Banks. Sell rates are 0.77, or 0.87 with Banana Salvage (bottom path tier 2 or higher).
- **Sources:** the [Bloons Wiki](https://www.bloonswiki.com/Banana_Farm_(BTD6)) and the [Fandom Bloons Wiki](https://bloons.fandom.com/wiki/Banana_Farm_(BTD6)). Values were also checked in game.
- **Simulation rules:** every farm is bought between rounds and works for the whole next round. We buy whenever we can afford a farm (greedy). Only farm income is counted (no pop cash or end-of-round cash). Banks are collected every k rounds, where k is chosen per bank.

## The candidate builds

`1-0-0`, `2-0-0`, `2-2-0`, `2-0-3`, `0-2-3`, `2-0-4`, `2-0-2`, `4-2-0`, `2-3-0` (bank), `2-4-0` (bank).

The notation is `[top path]-[middle path]-[bottom path]`. To add a build, add a row to `data/farms.csv` (the name must be in `a-b-c` format and the crosspath must be legal in the game).

## Limitations

- Perfect banana collection, so farm placement does not matter.
- No IMF Loan deposits, abilities, synergies, strategies, bosses, or other income towers.
- The model is not a guide to the best in-game farming strategy. Comparing builds is the method used to test the efficiency metric.
- The game shows bank balances rounded down, while the model keeps decimals (a difference below 1 per round).

## Media
Inside the **media** folder there are **images** and **videos** used in the project. Videos are used to showcase the measurements in-game in the ***In-game Verification*** section. The videos won't embed if using the preview from GitHub - instead manually open them from the file system or run the project on your device.