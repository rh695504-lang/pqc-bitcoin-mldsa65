# PQC-Bitcoin Research Lab — ML-DSA-65

**Status:** educational, off-chain research prototype. Not a Bitcoin wallet. Not compatible with Bitcoin mainnet or testnet spending.

This project measures the cost of using NIST ML-DSA-65 signatures on transaction-like messages. It does **not** create Bitcoin addresses, keys accepted by Bitcoin nodes, or spendable outputs.

## Research question

What are the key-size, signature-size, signing-time, and verification-time costs of using ML-DSA-65 to authorize a Bitcoin-like transaction message, and what protocol changes would be needed before such signatures could be accepted by Bitcoin?

## Important security warning

The prototype uses [`dilithium-py`](https://github.com/GiacomoPope/dilithium-py), a pure-Python educational implementation. Its own maintainers explicitly warn that it is not suitable for cryptographic applications and is not designed to resist side-channel attacks. Do not use it to protect funds, generate a real wallet, or store valuable secrets.

No private key is written to disk or printed. The code only reports public-key/signature sizes and timing measurements. Even so, run experiments on disposable research data only.

## Android / Termux setup

```bash
pkg update -y
pkg install python git -y
python -m pip install --upgrade pip
git clone <YOUR_REPOSITORY_URL>
cd pqc-bitcoin-mldsa65
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/benchmark.py --iterations 20 --output results/termux-benchmark.json
python -m unittest discover -s tests -v
```

If `dilithium-py` installation fails on your Termux/Python version, capture the full error and record the Android version, CPU/ABI, and Python version. Do not silently substitute another algorithm or implementation.

## Run

```bash
python src/benchmark.py --iterations 20
```

The benchmark:
1. Generates an ephemeral ML-DSA-65 keypair.
2. Signs a domain-separated, transaction-like byte message.
3. Verifies the signature.
4. Checks that a modified message is rejected.
5. Reports median and mean timing plus key/signature byte lengths.

The benchmark intentionally does not serialize the secret key. It does not claim constant-time behavior.

## What the results mean

ML-DSA-65 has standardized sizes of:
- Public key: 1,952 bytes
- Expanded private key: 4,032 bytes
- Signature: 3,309 bytes

These are algorithm-level sizes from FIPS 204. This project's observed timings are device-, interpreter-, and implementation-specific. They are not Bitcoin consensus benchmarks.

## Research boundaries

- No Bitcoin address is derived from an ML-DSA public key.
- No Bitcoin transaction is constructed or broadcast.
- No live Bitcoin node will accept this signature under today's consensus rules.
- A future Bitcoin deployment would require a protocol change defining output/script semantics, signature hashing, witness encoding, resource limits, relay/mining policy, wallet derivation, migration, and activation.
- A hash commitment to an ML-DSA public key is not, by itself, a spendable Bitcoin output.

## Repository structure

```text
.
├── README.md
├── RESEARCH_PLAN.md
├── PAPER_DRAFT.md
├── REFERENCES.md
├── requirements.txt
├── src/
│   └── benchmark.py
├── tests/
│   └── test_prototype.py
└── results/
    └── .gitkeep
```

## Reproducibility checklist

For every run, record:
- Date/time (UTC)
- Phone model and Android version
- Termux version
- Python version
- Package versions
- CPU architecture
- Iteration count
- Raw JSON output

Run at least 3 independent sessions. Avoid comparing results from different devices as if they were controlled experiments.

## License

Research scaffold: MIT. Third-party dependencies retain their own licenses. Review dependency licenses before redistribution.
