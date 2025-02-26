```
usage: arktrades [-n NUM] [-s] [-h] [--export {csv,json,xlsx}]
```

Get trades for ticker across all ARK funds.

```
optional arguments:
  -n NUM, --num NUM     Number of rows to show
  -s, --show_ticker     Flag to show ticker in table
  -h, --help            show this help message
  --export {csv,json,xlsx}
                        Export raw data into csv, json, xlsx
```
Output:

```python
(✨) (stocks)>(dd)> arktrades -n 5
╒════════════╤══════════╤══════════╤════════╤═════════════╤═════════════╤═══════════════╕
│            │   shares │   weight │ fund   │ direction   │   Close ($) │   Total ($1M) │
╞════════════╪══════════╪══════════╪════════╪═════════════╪═════════════╪═══════════════╡
│ 2020-08-24 │     9891 │   0.1830 │ ARKQ   │ Sell        │      125.86 │          1.24 │
├────────────┼──────────┼──────────┼────────┼─────────────┼─────────────┼───────────────┤
│ 2020-08-24 │    14278 │   0.2500 │ ARKW   │ Sell        │      125.86 │          1.80 │
├────────────┼──────────┼──────────┼────────┼─────────────┼─────────────┼───────────────┤
│ 2020-08-25 │    27722 │   0.4970 │ ARKF   │ Sell        │      124.82 │          3.46 │
├────────────┼──────────┼──────────┼────────┼─────────────┼─────────────┼───────────────┤
│ 2020-09-08 │    14631 │   0.2000 │ ARKQ   │ Sell        │      112.82 │          1.65 │
├────────────┼──────────┼──────────┼────────┼─────────────┼─────────────┼───────────────┤
│ 2020-09-08 │    90983 │   0.8200 │ ARKW   │ Sell        │      112.82 │         10.26 │
╘════════════╧══════════╧══════════╧════════╧═════════════╧═════════════╧═══════════════╛
```
