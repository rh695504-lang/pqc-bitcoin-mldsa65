# Research methodology

## 1. Aim

Evaluate the feasibility costs and integration constraints of ML-DSA-65 as a hypothetical post-quantum authorization primitive for Bitcoin-like transaction messages.

## 2. Hypotheses

- H1: ML-DSA-65 produces substantially larger public keys and signatures than Bitcoin's current ECDSA/Schnorr signature material.
- H2: On-device signing and verification latency on Android/Termux is measurable but implementation-dependent.
- H3: Cryptographic substitution alone is insufficient: Bitcoin consensus and transaction serialization must explicitly support the new signature scheme.

## 3. Scope

Included:
- ML-DSA-65 key generation, signing, verification
- Message-domain separation
- Negative verification test
- Key/signature byte-size accounting
- Android/Termux timing observations
- Protocol-level discussion of required changes

Excluded:
- Mainnet/testnet wallet creation
- Bitcoin address derivation
- Transaction broadcast or spendability claims
- Security certification or side-channel evaluation
- A claim that ML-DSA-65 is already part of Bitcoin consensus

## 4. Experimental design

Independent variable:
- Device/runtime environment (phone model, Android release, CPU ABI, Python version)

Measured dependent variables:
- Key-generation duration
- Signing duration
- Verification duration
- Public-key bytes
- Expanded private-key bytes (reported as a standard constant, not exported)
- Signature bytes
- End-to-end operation success/failure

Controls:
- Fixed message format and payload length
- Same ML-DSA-65 implementation and package version within a comparison
- Warm-up operation before timing
- Monotonic high-resolution timer
- Median and arithmetic mean reported
- Minimum 20 iterations for exploratory tests; 100+ recommended for more stable results

## 5. Message construction

The prototype signs:

`"PQC-BTC-RESEARCH-v1|" || UTF8(transaction_like_payload)`

This prefix is domain separation for the experiment only. It is not a Bitcoin sighash algorithm and must not be represented as one.

## 6. Procedure

1. Record device and software metadata.
2. Install the pinned dependency.
3. Run the benchmark with a stated iteration count.
4. Confirm a valid signature verifies.
5. Confirm the same signature fails on a changed message.
6. Save JSON output.
7. Repeat in three sessions.
8. Report median, mean, and spread; preserve raw outputs.
9. Compare measured signature/public-key sizes with the FIPS 204 sizes.
10. Discuss what consensus changes would be needed.

## 7. Analysis

Report:
- Median and mean keygen/sign/verify time
- Standard deviation or interquartile range in a later analysis pass
- Public key and signature sizes in bytes and approximate witness payload
- Verification throughput as `1 / median_verify_seconds`
- Caveats about interpreter overhead and educational implementation quality

Do not extrapolate phone microbenchmarks to Bitcoin network throughput. Do not compare against ECDSA unless the ECDSA baseline is implemented with a documented, audited library and identical hardware/test conditions.

## 8. Bitcoin protocol considerations

A credible proposal must specify:
- New output or script semantics
- Exact public-key commitment and reveal rules
- Signature message construction and transaction fields covered
- Witness serialization and weight accounting
- Consensus validation rules
- Mempool and relay policy
- Script/VM resource limits
- Wallet key derivation and backup format
- Migration path for existing UTXOs
- Test vectors, fuzzing, independent cryptographic review, and activation process

BIP 360's P2MR proposal is relevant background, but P2MR does not itself add ML-DSA signature verification. Study its stated threat model carefully.

## 9. Limitations

The selected Python implementation is explicitly educational and not side-channel hardened. Android timing is noisy. This prototype does not implement consensus rules, Bitcoin script, transaction serialization, or a secure wallet. Results support research discussion only.

## 10. Expected contribution

A reproducible Android/Termux measurement dataset and a carefully bounded integration analysis—not a claim of a new cryptographic algorithm or a deployable Bitcoin wallet.
