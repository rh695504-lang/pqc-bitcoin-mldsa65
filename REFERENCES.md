# References and source notes

1. **NIST FIPS 204 — Module-Lattice-Based Digital Signature Standard**  
   https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf  
   Normative source for ML-DSA. ML-DSA-65 encodings: 4,032-byte expanded private key, 1,952-byte public key, 3,309-byte signature.

2. **Bitcoin BIP 360 — Pay-to-Merkle-Root (P2MR)**  
   https://bitcoin.org/bip/360/  
   Proposal discussing long-exposure quantum attacks and the distinction between P2MR and future post-quantum signature support. Check the current proposal status before citing it as accepted or activated.

3. **dilithium-py source repository**  
   https://github.com/GiacomoPope/dilithium-py  
   Pure-Python ML-DSA educational implementation. Its README warns that it is not for cryptographic applications and is not side-channel secure. The prototype uses it only for educational experiments.

4. **RFC 9964 — ML-DSA for JOSE and COSE**  
   https://www.rfc-editor.org/rfc/rfc9964.html  
   Useful additional reference for ML-DSA encodings and key/signature sizes.
