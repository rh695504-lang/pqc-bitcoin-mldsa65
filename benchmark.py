#!/usr/bin/env python3
"""Educational ML-DSA-65 benchmark. Never use for real funds or production keys."""
from __future__ import annotations

import argparse
import json
import platform
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from dilithium_py.ml_dsa import ML_DSA_65
except ImportError as exc:
    raise SystemExit(
        "Missing dependency. Run: python -m pip install -r requirements.txt"
    ) from exc

DOMAIN = b"PQC-BTC-RESEARCH-v1|"
PAYLOAD = (
    b"research-only:version=1;network=not-specified;"
    b"inputs=example;outputs=example;nonce=0001"
)
MESSAGE = DOMAIN + PAYLOAD

# FIPS 204 standardized encoded sizes for ML-DSA-65.
PUBLIC_KEY_BYTES = 1952
EXPANDED_PRIVATE_KEY_BYTES = 4032
SIGNATURE_BYTES = 3309


def summarize(samples: list[float]) -> dict[str, float]:
    return {
        "mean_ms": round(statistics.mean(samples) * 1000, 4),
        "median_ms": round(statistics.median(samples) * 1000, 4),
        "min_ms": round(min(samples) * 1000, 4),
        "max_ms": round(max(samples) * 1000, 4),
    }


def run(iterations: int) -> dict:
    if iterations < 1 or iterations > 10000:
        raise ValueError("iterations must be between 1 and 10000")

    # Warm-up, excluded from timing.
    warm_pk, warm_sk = ML_DSA_65.keygen()
    warm_sig = ML_DSA_65.sign(warm_sk, MESSAGE)
    if not ML_DSA_65.verify(warm_pk, MESSAGE, warm_sig):
        raise RuntimeError("Warm-up signature verification failed")
    del warm_sk, warm_sig

    keygen_times: list[float] = []
    sign_times: list[float] = []
    verify_times: list[float] = []
    public_key_len = signature_len = None

    for _ in range(iterations):
        start = time.perf_counter()
        pk, sk = ML_DSA_65.keygen()
        keygen_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        signature = ML_DSA_65.sign(sk, MESSAGE)
        sign_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        valid = ML_DSA_65.verify(pk, MESSAGE, signature)
        verify_times.append(time.perf_counter() - start)

        if not valid:
            raise RuntimeError("Valid signature was rejected")

        if ML_DSA_65.verify(pk, MESSAGE + b"-tampered", signature):
            raise RuntimeError("Tampered message was incorrectly accepted")

        public_key_len = len(pk)
        signature_len = len(signature)

        # Do not serialize, print, or save the secret key.
        del sk, signature, pk

    return {
        "project": "PQC-Bitcoin Research Lab",
        "algorithm": "ML-DSA-65",
        "mode": "off-chain educational benchmark",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "iterations": iterations,
        "message_bytes": len(MESSAGE),
        "message_domain": DOMAIN.decode("ascii").rstrip("|"),
        "measurements": {
            "keygen": summarize(keygen_times),
            "sign": summarize(sign_times),
            "verify": summarize(verify_times),
        },
        "encodings": {
            "public_key_bytes_observed": public_key_len,
            "public_key_bytes_fips204": PUBLIC_KEY_BYTES,
            "expanded_private_key_bytes_fips204_not_exported": EXPANDED_PRIVATE_KEY_BYTES,
            "signature_bytes_observed": signature_len,
            "signature_bytes_fips204": SIGNATURE_BYTES,
        },
        "checks": {
            "valid_signature_accepted": True,
            "tampered_message_rejected_every_iteration": True,
        },
        "limitations": [
            "Not a Bitcoin address or wallet",
            "Not compatible with current Bitcoin consensus",
            "No transaction serialization or network broadcast",
            "Educational pure-Python implementation; not side-channel hardened",
            "Timings are device and runtime specific",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    result = run(args.iterations)
    rendered = json.dumps(result, indent=2)
    print(rendered)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"\nSaved results to: {args.output}")


if __name__ == "__main__":
    main()
