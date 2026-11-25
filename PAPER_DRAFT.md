# Measuring ML-DSA-65 for a Hypothetical Post-Quantum Bitcoin Authorization Layer

**Author:** [Researcher name]  
**Version:** 0.1 — preliminary research draft  
**Date:** [Insert date]

## Abstract

Bitcoin's current transaction authorization relies on elliptic-curve digital signatures. A sufficiently capable cryptographically relevant quantum computer could threaten discrete-logarithm-based signature systems. This preliminary study outlines an experimental evaluation of NIST's Module-Lattice-Based Digital Signature Algorithm, ML-DSA-65, as a candidate authorization primitive for a hypothetical future Bitcoin protocol extension. We provide an Android/Termux-oriented, off-chain prototype that generates ephemeral ML-DSA-65 keys, signs a domain-separated transaction-like message, verifies signatures, rejects modified messages, and records operation timings and encoded sizes. The prototype does not create Bitcoin addresses, construct spendable Bitcoin transactions, or claim compatibility with current Bitcoin consensus. The study's intended contribution is reproducible resource measurement and a protocol integration checklist. Measurements must be collected on the target device before quantitative conclusions can be drawn.

**Keywords:** post-quantum cryptography, Bitcoin, ML-DSA, FIPS 204, digital signatures, Android, benchmarking.

## 1. Introduction

Bitcoin's authorization model uses public-key cryptography to prove control over unspent transaction outputs. Quantum algorithms create a long-term research concern for cryptographic systems based on the elliptic-curve discrete logarithm problem. Post-quantum digital signatures offer a possible alternative, but their public keys and signatures can be much larger than conventional elliptic-curve signatures.

ML-DSA, standardized by NIST in FIPS 204, is a lattice-based digital signature scheme. The ML-DSA-65 parameter set is assigned security category 3 in the NIST framework. Its standardized public key is 1,952 bytes and its signature is 3,309 bytes. These sizes make transaction weight, bandwidth, storage, validation cost, and fee-market effects important questions.

This paper studies ML-DSA-65 as a hypothetical authorization mechanism. It does not assert that Bitcoin currently supports this scheme.

## 2. Research questions

1. What are the key-generation, signing, and verification costs of ML-DSA-65 on an Android device running Python in Termux?
2. What are the public-key and signature payload sizes?
3. What protocol and consensus changes would be required before a Bitcoin node could validate ML-DSA-65 spends?
4. What limitations arise from using a pure-Python educational implementation?

## 3. Background

FIPS 204 specifies ML-DSA-44, ML-DSA-65, and ML-DSA-87. ML-DSA-65 has a 1,952-byte public key, a 4,032-byte expanded private key, and a 3,309-byte signature. These values describe standardized encodings, not Bitcoin transaction sizes.

Bitcoin Improvement Proposal 360 discusses Pay-to-Merkle-Root (P2MR), a proposed output construction intended to reduce certain long-exposure quantum risks by avoiding Taproot's exposed key-path design. P2MR is not itself a post-quantum signature scheme. The BIP text explicitly distinguishes long-exposure protection from short-exposure attacks and notes that full protection may require post-quantum signatures.

## 4. Method

The prototype imports the `ML_DSA_65` implementation from `dilithium-py`. For each iteration it:
1. Generates an ephemeral key pair.
2. Creates a fixed-format transaction-like message with an experiment-specific domain-separation prefix.
3. Signs the message.
4. Verifies the signature.
5. Attempts verification against a modified message and expects rejection.
6. Records elapsed time using Python's monotonic performance counter.

The secret key is held only in process memory and is not printed or saved. The prototype is for educational benchmarking and must not be used to secure funds.

## 5. Results

**No experimental results are claimed in this draft.** Populate this section only after running the experiment on the target Android device.

Recommended table:

| Metric | Median | Mean | Notes |
|---|---:|---:|---|
| Key generation (ms) | [measure] | [measure] | Per operation |
| Signing (ms) | [measure] | [measure] | Per operation |
| Verification (ms) | [measure] | [measure] | Per operation |
| Public key (bytes) | 1952 | 1952 | FIPS 204 encoding |
| Signature (bytes) | 3309 | 3309 | FIPS 204 encoding |

Include phone model, Android version, CPU architecture, Python version, package version, iteration count, and raw JSON data.

## 6. Discussion

The main expected integration challenge is data size. A 3,309-byte signature is much larger than the signature data used by current Bitcoin authorization paths. The exact fee and block-weight impact cannot be stated without a proposed witness format and consensus accounting rules.

A Bitcoin deployment would also need an agreed signature-hash construction, public-key commitment rules, witness serialization, validation semantics, resource limits, relay policy, wallet support, migration strategy, test vectors, and network activation. An off-chain Python signature demonstration cannot establish any of these properties.

## 7. Threats to validity

The selected `dilithium-py` project explicitly describes itself as educational, not constant-time, and unsuitable for cryptographic applications. Its performance is not representative of optimized C or hardware implementations. Python interpreter overhead and Android thermal/power management can affect timing. The prototype does not model Bitcoin Core validation or transaction propagation.

## 8. Conclusion

This work establishes a reproducible starting point for measuring ML-DSA-65 on Android and examining the protocol changes required for a post-quantum Bitcoin authorization path. It does not produce a Bitcoin-compatible wallet or demonstrate a live-network solution. Future work should repeat the measurements using a maintained, audited native implementation, add a documented classical baseline, develop a formal witness and sighash proposal, and obtain independent cryptographic and Bitcoin protocol review.

## References

1. NIST, **FIPS 204: Module-Lattice-Based Digital Signature Standard**, 2024.
2. Bitcoin BIP 360, **Pay-to-Merkle-Root (P2MR)**, proposal text.
3. Giacomo Pope, **dilithium-py**, educational pure-Python ML-DSA implementation. See its security disclaimer before use.
