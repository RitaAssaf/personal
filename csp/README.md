# Solve SIP problem with MiniZinc and PyCSP3

## Requirements

- Bash
- Python 3
- Minizinc

## Use

Run benchmark on PyCSP3:

```bash
bash run/benchmark.sh -e
```

Run benchmark on MiniZinc:

```bash
bash run/benchmark.sh -e -m mzn
```

## Modify

You can add and remove instances to benchmark by modifying lines at the end of `run/benchmark.sh`

You can also modify Minizinc model in `src/sip.mzn` and PyCSP3 in `src/sip.py`.
